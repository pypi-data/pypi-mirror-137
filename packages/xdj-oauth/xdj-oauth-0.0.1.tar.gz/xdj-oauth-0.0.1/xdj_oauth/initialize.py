# 初始化
import os

import django

from xdj_utils.core_initialize import CoreInitialize

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()


class Initialize(CoreInitialize):
    creator_id = "456b688c-8ad5-46de-bc2e-d41d8047bd42"

    def run(self):
        pass


# 项目init 初始化，默认会执行 main 方法进行初始化
def main(reset=False):
    Initialize(reset).run()
    pass


if __name__ == '__main__':
    main()
