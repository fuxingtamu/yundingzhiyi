from http.server import BaseHTTPRequestHandler, HTTPServer


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 处理 GET 请求的代码保持不变
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Hello, World! This is a simple HTTP server running on port 8080.")

    def do_POST(self):
        # 设置响应状态码为200
        self.send_response(200)
        # 设置响应头，这里可以根据需要设置不同的内容类型
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        # 读取请求体中的内容
        # 注意：这里使用了self.rfile来读取数据，但通常需要知道内容的长度
        # 这里我们假设内容很短，并且使用简单的读取方式
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # 打印接收到的数据
        print("Received POST data:", post_data.decode('utf-8'))

        # 向客户端发送响应体（可选）
        # 例如，我们可以回显接收到的数据
        self.wfile.write(b"POST data received and echoed back.")


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', 8080)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on {server_address[0]}:{server_address[1]}")
    httpd.serve_forever()


if __name__ == '__main__':
    run()