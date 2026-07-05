const http = require("http");
const fs = require("fs");
const path = require("path");

const rootDir = path.resolve(__dirname, "..");
const args = process.argv.slice(2);

function readArg(name, fallback) {
  const prefix = `--${name}=`;
  const inline = args.find((item) => item.startsWith(prefix));
  if (inline) return inline.slice(prefix.length);
  const index = args.indexOf(`--${name}`);
  if (index >= 0 && args[index + 1]) return args[index + 1];
  return fallback;
}

const host = readArg("host", "127.0.0.1");
const preferredPort = Number(readArg("port", process.env.PORT || "5173"));

const contentTypes = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".svg": "image/svg+xml",
  ".ico": "image/x-icon",
};

function resolveFile(urlPath) {
  const cleanPath = decodeURIComponent(urlPath.split("?")[0]).replace(/^\/+/, "");
  const targetPath = path.resolve(rootDir, cleanPath || "index.html");
  if (!targetPath.startsWith(rootDir)) return null;
  if (fs.existsSync(targetPath) && fs.statSync(targetPath).isFile()) return targetPath;
  return path.join(rootDir, "index.html");
}

function createServer() {
  return http.createServer((req, res) => {
    const filePath = resolveFile(req.url || "/");
    if (!filePath) {
      res.writeHead(403);
      res.end("Forbidden");
      return;
    }

    fs.readFile(filePath, (error, buffer) => {
      if (error) {
        res.writeHead(404);
        res.end("Not found");
        return;
      }
      res.writeHead(200, {
        "Content-Type": contentTypes[path.extname(filePath)] || "application/octet-stream",
        "Cache-Control": "no-store",
      });
      res.end(buffer);
    });
  });
}

function listen(port) {
  const server = createServer();
  server.on("error", (error) => {
    if (error.code === "EADDRINUSE" && port < preferredPort + 20) {
      listen(port + 1);
      return;
    }
    console.error(error.message);
    process.exit(1);
  });
  server.listen(port, host, () => {
    console.log(`Admin console running at http://${host}:${port}/`);
    console.log("Default API base: http://127.0.0.1:8000/api/v1");
  });
}

listen(preferredPort);
