import urllib
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import json
import mysql.connector


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

        conn = mysql.connector.connect(
            host="localhost",
            user="rtsw",
            password="123456",
            database="reposyncer"
        )
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS last_subject_list
                              (id INT AUTO_INCREMENT PRIMARY KEY, last_subject VARCHAR(100))''')

        information = json.loads(post_data.decode('utf-8'))
        different = information['url']
        if 'issue' in different:
            issue_information = information['issue']
            print(issue_information)

            if 'subject' in issue_information:
                cursor.execute('SELECT last_subject FROM last_subject_list ORDER BY id DESC LIMIT 1')
                result = cursor.fetchone()
                subject_last = result[0]
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

                    sql = "INSERT INTO last_subject_list (last_subject) VALUES (%s)"

                    # 执行 SQL 语句，注意 issue_subject 需要被放在一个元组中
                    cursor.execute(sql, (issue_information['subject'],))
            else:
                cursor.execute('SELECT last_subject FROM last_subject_list ORDER BY id DESC LIMIT 1')
                result = cursor.fetchone()
                subject_last = result[0]
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
                    sql = "INSERT INTO last_subject_list (last_subject) VALUES (%s)"
                    # 执行 SQL 语句，注意 issue_subject 需要被放在一个元组中
                    cursor.execute(sql, (issue_information['title'],))
            # 提交事务
            conn.commit()
            # 关闭游标和连接
            cursor.close()
            conn.close()

        else:

            if 'gitee' in different:
                pr_target_branch = information['target_branch']
                pr_source_branch = information['source_branch']
                pr_title = information['title']
                pr_body = information['body']
                url = "https://gitlink.org.cn/api/xumingyang21/reposyncer2/pulls.json"
                payload = json.dumps({
                    "title": pr_title,
                    "priority_id": "2",
                    "body": pr_body,
                    "head": pr_source_branch,
                    "base": pr_target_branch,
                    "is_original": False,
                    "fork_project_id": "",
                    "files_count": 1,
                    "commits_count": 1,
                    "reviewer_ids": [],
                    "receivers_login": []
                })
                access_token = '_LSPz_Q_g9h7j-Zo64hO2MDPMjDTS_o6rqD809mxWgQ'
                headers = {
                    'Authorization': f'Bearer {access_token}',  # 使用 Bearer 标记
                    'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
                    'Content-Type': 'application/json'
                }

                response = requests.request("POST", url, headers=headers, data=payload)
                data = response.json()
                print(data)
                print(response.text)

            else:

                gitlink_pr_info = information['pull_request']
                pr_title = gitlink_pr_info['title']
                pr_body = gitlink_pr_info['body']
                head_info = gitlink_pr_info['head']
                pr_head = head_info['label']
                base_info = gitlink_pr_info['base']
                pr_base = base_info['label']

                owner = 'xumingyang21'
                repo = 'reposyncer2'
                # Gitee获取issue的API URL
                url = f'https://gitee.com/api/v5/repos/{owner}/{repo}/pulls'
                # 构造请求头
                token = 'f2be2313581c1fde50b16bf35bb655c5'
                headers = {'Authorization': f'token {token}'}
                # 发送POST请求 获取状态为open的issue
                data = {
                    "access_token": token,
                    "owner": owner,
                    "repo": repo,
                    "title": pr_title,
                    "body": pr_body,
                    "head": pr_head,
                    "base": pr_base
                }

                # 将字典转换为查询字符串
                query_string = urllib.parse.urlencode(data)
                # 完整的请求 URL，包括查询字符串
                full_url = f"{url}?{query_string}"
                response = requests.post(full_url, headers=headers, json=data)
                if response.status_code == 201:
                    pr_info = response.json()
                    print(pr_info)
                else:
                    print(f"获取pr失败，状态码：{response.status_code}，错误信息：{response.text}")

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