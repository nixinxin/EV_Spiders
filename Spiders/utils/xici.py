# -*- coding: utf-8 -*-
import requests
import MySQLdb

conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="123456", db="elevator", charset="utf8")
cursor = conn.cursor()

def crawl_ips(num):
    # 爬取西刺的免费ip代理
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
    result = requests.get("http://tvp.daxiangdaili.com/ip/?tid=557485331689053&num={}&operator=3&delay=1&category=2".format(num), headers=headers).text
    for i in result.split("\n"):
        ip, port = i.split(":")
        cursor.execute(
            "insert proxy_ip(ip, port) VALUES('{0}', '{1}') on duplicate key update `ip`=values(`ip`)".format(
               ip, port))
        conn.commit()
        print(i)


class GetIP(object):
    def delete_ip(self, ip):
        # 从数据库中删除无效的ip
        delete_sql = """delete from proxy_ip where ip='{0}' """.format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def judge_ip(self, ip, port):
        # 判断ip是否可用
        http_url = "https://cn.bing.com/"
        proxy_url = "http://{0}:{1}".format(ip, port)
        try:
            proxy_dict = {
                "http": proxy_url,
            }
            response = requests.get(http_url, proxies=proxy_dict)
        except Exception as e:
            print(e)
            print("invalid ip and port")
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if 200 <= code < 300:
                print("effective ip", proxy_url)
                return True
            else:
                print("invalid ip and port")
                self.delete_ip(ip)
                return False

    def get_random_ip(self):
        # 从数据库中随机获取一个可用的ip
        random_sql = """SELECT ip, port FROM proxy_ip ORDER BY RAND() LIMIT 1"""
        cursor.execute(random_sql)
        conn.commit()
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]

            judge_re = self.judge_ip(ip, port)
            if judge_re:
                return "http://{0}:{1}".format(ip, port)
            else:
                return self.get_random_ip()


if __name__ == "__main__":
    try:
        crawl_ips(100)
        get_ip = GetIP()
        get_ip.get_random_ip()
    except Exception as e:
        print(Exception)