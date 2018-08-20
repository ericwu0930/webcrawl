from selenium import webdriver
from bs4 import BeautifulSoup
import json


class SCU:
    def __init__(self, user, password, name):
        self.name = name
        self.url = 'http://zhjw.scu.edu.cn/login.jsp'
        self.user = user
        self.password = password

    def get_page(self):
        self.browser = webdriver.Chrome()
        self.browser.get(self.url)
        user = self.browser.find_element_by_xpath(
            '/html/body/table/tbody/tr/td/table[3]/tbody/tr[1]/td[2]/form/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/input'
        )
        password = self.browser.find_element_by_xpath(
            '/html/body/table/tbody/tr/td/table[3]/tbody/tr[1]/td[2]/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/input'
        )
        user.send_keys(self.user)
        password.send_keys(self.password)
        button = self.browser.find_element_by_xpath('//*[@id="btnSure"]')
        button.click()
        self.browser.switch_to.frame('bottomFrame')
        self.browser.switch_to.frame('mainFrame')
        ref = self.browser.find_element_by_link_text('方案成绩')
        ref.click()
        self.browser.switch_to.frame('lnfaIfra')

    def parse_score(self):
        self.soup = BeautifulSoup(self.browser.page_source, 'lxml')
        for i in self.soup.find_all(name='tr', attrs={'class': 'odd'}):
            yield {
                'subject': i.contents[5].string.strip(),
                'credit': i.contents[9].string.strip(),
                'grade': i.contents[13].p.string.strip()
            }

    def write_to_file(self):
        for item in self.parse_score():
            with open('gpa_' + self.name + '.txt', 'a', encoding='utf-8') as f:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')

    def gpa(self):
        sum_credit = 0
        grade = 0
        for i in self.soup.find_all(name='tr', attrs={'class': 'odd'}):
            if i.contents[13].p.string.strip() == '中等': grade += 2.7 * float(i.contents[9].string.strip())
            elif i.contents[13].p.string.strip() == '良好': grade += 3.7 * float(i.contents[9].string.strip())
            elif i.contents[13].p.string.strip() == '优秀': grade += 4 * float(i.contents[9].string.strip())
            elif 90 <= float(i.contents[13].p.string.strip()) <= 100: grade += 4 * float(i.contents[9].string.strip())
            elif 85 <= float(i.contents[13].p.string.strip()) <= 89: grade += 3.7 * float(i.contents[9].string.strip())
            elif 82 <= float(i.contents[13].p.string.strip()) <= 84: grade += 3.3 * float(i.contents[9].string.strip())
            elif 78 <= float(i.contents[13].p.string.strip()) <= 81: grade += 3.0 * float(i.contents[9].string.strip())
            elif 75 <= float(i.contents[13].p.string.strip()) <= 77: grade += 2.7 * float(i.contents[9].string.strip())
            elif 72 <= float(i.contents[13].p.string.strip()) <= 74: grade += 2.3 * float(i.contents[9].string.strip())
            elif 68 <= float(i.contents[13].p.string.strip()) <= 71: grade += 2.0 * float(i.contents[9].string.strip())
            elif 64 <= float(i.contents[13].p.string.strip()) <= 67: grade += 1.5 * float(i.contents[9].string.strip())
            elif 60 <= float(i.contents[13].p.string.strip()) <= 63: grade += 1 * float(i.contents[9].string.strip())
            sum_credit += float(i.contents[9].string.strip())
        overall = {'gpa': grade / sum_credit}
        with open('gpa_' + self.name + '.txt', 'a', encoding='utf-8') as f:
            f.write(json.dumps(overall, ensure_ascii=False))
        self.browser.close()
scu=SCU(input("请输入学号："),input("请输入密码："),input("请输入你的名字："))
scu.get_page()
scu.write_to_file()
scu.gpa()

