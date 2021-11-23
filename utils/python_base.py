# __init__ 初始化参数，是给强制绑定的属性，就是实例化类的时候，必须传进去这些属性。这些属性也是这些类别区别其他类的特征
class Hero(object):
    def __init__(self, mingzi, paiwei, dazhao):
        self.name = mingzi
        self.weight = paiwei
        self.skill = dazhao
    # 跑

    def run(self):
        print('{}快跑,并且释放你的大招{}'.format(self.name, self.skill))
    # 攻击

    def attack(self):
        print('{}使用{}向你攻击'.format(self.name, self.skill))
    # 回城

    def home(self):
        print('{}血量不足，要回城了'.format(self.name))
    # 排位

    def rank(self):
        print('{}目前的排位是{}'.format(self.name, self.weight))

    def work(self):
        print(self.run(), self.attack(), self.home(), self.rank())


if __name__ == '__main__':
    hero1 = Hero('程咬金', '荣耀黄金iv', '战斧之刃')
    hero2 = Hero('孙悟空', '钻石iv', '天崩地裂')
    # 程咬金整套动作
    print(hero1.work())
    # 孙悟空整套动作
    print(hero2.work())
    # 程咬金回家
    print(hero2.home())
