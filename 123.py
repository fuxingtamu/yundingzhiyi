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

    def do_POST(self, subject_last=None):
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

        information = json.load(post_data.decode('utf-8'))
        issue_information = information['issue']
        print(issue_information)

        if 'subject' in  issue_information:
            if subject_last != issue_information['subject']:
                # 你的仓库信息
                owner = 'xumingyang21'
                repo = 'reposyncer2'

                # 创建issue的标题和内容
                issue_title = issue_information['subject']
                issue_body = issue_information['description']

                # Gitee创建issue的API URL
                url = f"https://gitee.com/api/v5/repos/{owner}/issues"

                # 构造请求头
                token = 'f2be2313581c1fde50b16bf35bb655c5'
                headers = {'Authorization': f'token {token}'}

                # 发送POST请求
                data = {
                    "access_token": token,
                    "owner": owner,
                    "repo": repo,
                    "title": issue_title,
                    "body": issue_body
                }

                response = requests.post(url, headers=headers, json=data)
                # 打印响应
                print(response.text)
                # 检查响应状态码
                if response.status_code == 201:
                    # 注意：这里假设响应体中包含一个'number'字段作为issue的ID，但实际上Gitee可能返回不同的结构
                    # 你需要根据实际的响应结构来调整以下代码
                    issue_info = response.json()
                    print(f'Issue created with ID: {issue_info["number"]}')
                else:
                    print(f"创建issue失败，状态码：{response.status_code}，错误信息：{response.text}")

                subject_last = issue_information['subject']
        else:
            if subject_last != issue_information['title']:
                subject = issue_information['title']
                description = issue_information['body']
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
                subject_last = subject

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