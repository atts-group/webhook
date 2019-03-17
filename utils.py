
def make_push_bear_report(status_message, build_url, started_at, duration, author_name, compare_url):
    return f"""
* 当前构建地址：{build_url}
* 启动时间：{started_at}，耗时 {duration} 秒

由 {author_name} [修改代码]({compare_url}) 触发构建，当前构建状态 {status_message}
"""
