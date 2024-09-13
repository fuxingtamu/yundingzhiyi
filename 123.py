from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import json



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

        information = post_data.decode('utf-8')
        issue_imformation = information['issue']
        print(issue_imformation)
        subject = issue_imformation['title']
        description = information['body']
        url = "https://gitlink.org.cn/api/v1/xumingyang21/reposyncer2/issues.json"

        payload = json.dumps({
            "status_id": 1,  # status对应 1对应新增 2对应正在解决 3对应已解决
            "priority_id": 2,  # priority对应 1对应低 2对应正常 3对应高优先级
            "subject": subject,
            "description": description,
        })
        # 替换为您的实际访问令牌
        access_token = '4beTv9a8_I7BaEzmdSLMQ2w9meqIoEu5BUKPr5ctAv4'
        headers = {
            'Authorization': f'Bearer {access_token}',  # 使用 Bearer 标记
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
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