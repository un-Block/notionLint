from notion.client import NotionClient
import re
# DEFI->Defi
# space between Chinese and English, number
# Chinese Punctuations

# Some Helper functions


def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def is_al_num(word):
    # 因为定义的一些变量或者方法可能带有下划线
    # 还有一些分割的时候，把两个单次分割到了一块，所以带有空格，还有一些带(),所以先把这些去掉，再进行判断
    word = word.replace("_", "").replace(
        " ", "").replace("()", "").encode('UTF-8')
    if word.isalpha():
        return True
    if word.isdigit():
        return True
    if word.isalnum():
        return True
    return False

# Component for lint


def typo(text):
    # fix typo
    # return correct string
    # Optimization: use REG,use for loop
    text = 'DeFi'.join(text.split('DEFI'))
    text = 'DeFi'.join(text.split('Defi'))
    return text


def add_space(text, pattern=r"([\u4e00-\u9fff])", isloop=True):
    # add space between Chinese, English, Number
    # source:http://hoyouly.fun/2020/04/11/python-beatiful-text/
    """
        美化文案，中英文，英文与数字，中文与数字直接都添加空格
        :param text: 要美化的原始文案
        :param pattern: 替换规则
        :param isloop: 如果不符合规则的，是否根据新的规则继续美化
    """
    res = re.compile(pattern)  # [\u4e00-\u9fa5]中文范围

    p1 = res.split(text)
    result = ""
    for index in range(len(p1)):
        str = p1[index]
        if "\n" == str:
            result += str
            continue
        # if len(str.strip()) == 0:
        #     # 空白字符直接返回
        #     continue
        if is_Chinese(str):
            # 说明是中文
            result += str
        elif is_al_num(str):
            # 是纯英文，或者纯数字，或者英文和数字组合，则前后加上空格
            if isloop and index == 0:
                # 第一行的首个是数字或者英文，直接在后面添加空格，前面不需要
                result += (str.strip() + " ")
            else:
                result += (" " + str.strip() + " ")
        else:
            if isloop:
                # 使用新的规则，继续美化，这里主要是根据一些中文，英文常用符号
                result += add_space(str, r"([。，？！,!]+)", False)
            else:
                result += str
    return result


def lint(text):
    # lint the content
    # return format string
    text = typo(text)
    text = add_space(text)
    return text


if __name__ == '__main__':
    # Obtain the `token_v2` value by inspecting your browser cookies on a logged-in (non-guest) session on Notion.so
    client = NotionClient(
        token_v2="89fc7f65d1b4a6e1540bb5ca7f7af180380f37f0b89e2422573f0b59ecbdf534671c6b17a02d9c945c5e46641358fd5321e54159a7a896564bedf08b6d2a1bd00d8b67362d514162578b0ffde802")

    # Replace this URL with the URL of the page you want to edit
    page = client.get_block(
        "https://www.notion.so/glazec/Linter-1c4851cc2576469585651f6048d889f5")

    print("Linting Page:", page.title)
    # filter out the text,quote,bullet list,heading
    for child in page.children:
        # linter the text block and quote block
        if child._type == 'text' or child._type == 'quote':
            # exclude empty block
            if child.title != '':
                # lint(child.title)
                child.title = lint(child.title)
