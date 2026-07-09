// Template for ASP.NET MVC 5 / System.Web local or staging Golden Master capture.
// Do not enable this in production. Review and extend RedactValue for your app's secrets.
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Web;
using System.Web.Mvc;
using System.Web.Script.Serialization;

public sealed class LegacyTrafficDumperAttribute : ActionFilterAttribute
{
    private const string CaptureStreamKey = "__LegacyTrafficDumper_ResponseStream";
    private const string OriginalStreamKey = "__LegacyTrafficDumper_OriginalResponseStream";
    private readonly string _rootDirectory;
    private readonly JavaScriptSerializer _json = new JavaScriptSerializer();

    public LegacyTrafficDumperAttribute()
        : this("~/App_Data/GoldenMasterTraffic")
    {
    }

    public LegacyTrafficDumperAttribute(string rootDirectory)
    {
        _rootDirectory = rootDirectory;
    }

    public override void OnActionExecuting(ActionExecutingContext filterContext)
    {
        var context = filterContext.HttpContext;
        var request = context.Request;
        var captureDirectory = CreateCaptureDirectory(context);
        context.Items["__LegacyTrafficDumper_CaptureDirectory"] = captureDirectory;

        WriteJson(Path.Combine(captureDirectory, "request.json"), new
        {
            method = request.HttpMethod,
            rawUrl = request.RawUrl,
            contentType = request.ContentType,
            query = ToDictionary(request.QueryString),
            form = ToDictionary(request.Form),
            route = filterContext.RouteData.Values.ToDictionary(x => x.Key, x => Convert.ToString(x.Value)),
            body = ReadRequestBody(request)
        });

        WriteJson(Path.Combine(captureDirectory, "request-headers.json"), ToDictionary(request.Headers, redact: true));
        WriteJson(Path.Combine(captureDirectory, "request-cookies.json"), CookiesToDictionary(request.Cookies, redact: true));

        var original = context.Response.Filter;
        var capture = new CapturingResponseStream(original);
        context.Items[OriginalStreamKey] = original;
        context.Items[CaptureStreamKey] = capture;
        context.Response.Filter = capture;
    }

    public override void OnResultExecuted(ResultExecutedContext filterContext)
    {
        var context = filterContext.HttpContext;
        var captureDirectory = context.Items["__LegacyTrafficDumper_CaptureDirectory"] as string;
        if (string.IsNullOrWhiteSpace(captureDirectory))
        {
            return;
        }

        var response = context.Response;
        File.WriteAllText(Path.Combine(captureDirectory, "expected-status.txt"), response.StatusCode.ToString());
        WriteJson(Path.Combine(captureDirectory, "response-headers.json"), ToDictionary(response.Headers, redact: true));
        WriteJson(Path.Combine(captureDirectory, "response-cookies.json"), CookiesToDictionary(response.Cookies, redact: true));

        var capture = context.Items[CaptureStreamKey] as CapturingResponseStream;
        if (capture != null)
        {
            var body = capture.GetCapturedText(response.ContentEncoding ?? Encoding.UTF8);
            var extension = LooksLikeJson(body) ? "json" : "txt";
            File.WriteAllText(Path.Combine(captureDirectory, "response-body." + extension), body);
        }

        WriteJson(Path.Combine(captureDirectory, "dynamic-fields.json"), new object[0]);
        File.WriteAllText(Path.Combine(captureDirectory, "side-effects.md"), "# Side Effects\n\n- Not captured by this filter. Verify database, file, and external API effects separately.\n");
        File.WriteAllText(Path.Combine(captureDirectory, "notes.md"), "# Notes\n\nCaptured by LegacyTrafficDumperAttribute in local or staging runtime.\n");
    }

    private string CreateCaptureDirectory(HttpContextBase context)
    {
        var root = context.Server.MapPath(_rootDirectory);
        var safePath = context.Request.RawUrl
            .Replace("/", "_")
            .Replace("\\", "_")
            .Replace("?", "_")
            .Replace("&", "_")
            .Replace("=", "_")
            .Replace(":", "_");
        var directory = Path.Combine(root, DateTime.UtcNow.ToString("yyyyMMddTHHmmssfffZ") + "_" + context.Request.HttpMethod + safePath);
        Directory.CreateDirectory(directory);
        return directory;
    }

    private string ReadRequestBody(HttpRequestBase request)
    {
        if (request.InputStream == null || !request.InputStream.CanSeek)
        {
            return null;
        }

        var originalPosition = request.InputStream.Position;
        request.InputStream.Position = 0;
        using (var reader = new StreamReader(request.InputStream, request.ContentEncoding ?? Encoding.UTF8, true, 4096, true))
        {
            var body = reader.ReadToEnd();
            request.InputStream.Position = originalPosition;
            return body;
        }
    }

    private IDictionary<string, string> ToDictionary(System.Collections.Specialized.NameValueCollection values, bool redact = false)
    {
        return values.AllKeys
            .Where(key => key != null)
            .ToDictionary(key => key, key => redact ? RedactValue(key, values[key]) : values[key]);
    }

    private IDictionary<string, string> CookiesToDictionary(HttpCookieCollection cookies, bool redact)
    {
        return cookies.AllKeys
            .Where(key => key != null)
            .ToDictionary(key => key, key => redact ? RedactValue(key, cookies[key].Value) : cookies[key].Value);
    }

    private string RedactValue(string name, string value)
    {
        if (string.IsNullOrEmpty(value))
        {
            return value;
        }

        var lower = (name ?? string.Empty).ToLowerInvariant();
        if (lower.Contains("authorization") || lower.Contains("token") || lower.Contains("secret") ||
            lower.Contains("password") || lower.Contains("cookie") || lower.Contains("session"))
        {
            return "<redacted>";
        }

        return value;
    }

    private bool LooksLikeJson(string value)
    {
        if (string.IsNullOrWhiteSpace(value))
        {
            return false;
        }

        var trimmed = value.TrimStart();
        return trimmed.StartsWith("{", StringComparison.Ordinal) || trimmed.StartsWith("[", StringComparison.Ordinal);
    }

    private void WriteJson(string path, object value)
    {
        File.WriteAllText(path, _json.Serialize(value));
    }

    private sealed class CapturingResponseStream : Stream
    {
        private readonly Stream _inner;
        private readonly MemoryStream _capture = new MemoryStream();

        public CapturingResponseStream(Stream inner)
        {
            _inner = inner;
        }

        public override bool CanRead { get { return _inner.CanRead; } }
        public override bool CanSeek { get { return _inner.CanSeek; } }
        public override bool CanWrite { get { return _inner.CanWrite; } }
        public override long Length { get { return _inner.Length; } }
        public override long Position { get { return _inner.Position; } set { _inner.Position = value; } }

        public override void Flush()
        {
            _inner.Flush();
        }

        public override int Read(byte[] buffer, int offset, int count)
        {
            return _inner.Read(buffer, offset, count);
        }

        public override long Seek(long offset, SeekOrigin origin)
        {
            return _inner.Seek(offset, origin);
        }

        public override void SetLength(long value)
        {
            _inner.SetLength(value);
        }

        public override void Write(byte[] buffer, int offset, int count)
        {
            _capture.Write(buffer, offset, count);
            _inner.Write(buffer, offset, count);
        }

        public string GetCapturedText(Encoding encoding)
        {
            return encoding.GetString(_capture.ToArray());
        }
    }
}
