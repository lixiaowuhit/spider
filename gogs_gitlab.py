import requests
from pyquery import PyQuery as pq
import os


gogs_repos_url = "http://192.168.100.3:43000/explore/repos"
ua = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'
repos_dir = "repo_dir"  # 项目临时下载repo的 文件夹
repo_list = []     # 项目的每个repo的列表,每个元素是每个repo的文件夹,源url地址和gitlab的地址


def get_repo():
    with requests.get(gogs_repos_url, headers={'user-agent': ua}) as resp:
        html = pq(resp.text)
        for r in html("div.ui.repository.list>.item a").items():
            repo_name = str(r.attr("href"))
            repo_dir = repo_name.lstrip("/").split("/")[1]
            if repo_name.startswith("/root") or repo_name.startswith("/test_group"):
                repo_list.append((repo_dir,
                                  f"ssh://git@192.168.100.3:43022{repo_name}.git",
                                  f"ssh://git@192.168.100.3:2222{repo_name}.git"))
            else:
                repo_list.append((repo_dir, f"git@github.com:{repo_name.lstrip('/')}.git",
                                  f"ssh://git@192.168.100.3:2222{repo_name}.git"))


# clone 代码, 其中repos.txt是需要从github迁移到gitlab的repository的地址,git@开头
def clone():
    print("start clone.......")
    os.mkdir(repos_dir)
    os.chdir(repos_dir)
    for repo in repo_list:
        os.system(f"git clone {repo[1]}")


def push():
    final_repo_dir = os.getcwd() + "/" + repos_dir
    for repo in repo_list:
        print(f"start push {repo[2]}")

        try:
            os.chdir(final_repo_dir + "/" + repo[0])  # 切换到clone后的项目目录
        except Exception as e:
            print(e)
            continue
        print(f"current dir is {os.getcwd()} ")
        os.system(f"git push {repo[2]} master")


if __name__ == "__main__":
    # get_repo()
    # print(repo_list)
    # clone()
    push()