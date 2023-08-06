# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jinf']

package_data = \
{'': ['*'], 'jinf': ['data/*']}

install_requires = \
['pyknp>=0.5.0']

setup_kwargs = {
    'name': 'jinf',
    'version': '0.1.0',
    'description': 'A Japanese inflection converter.',
    'long_description': '# Jinf: Japanese Inflection Converter\n\n**Jinf** is a Japanese inflection converter.\nJinf depends on [JumanDic](https://github.com/ku-nlp/JumanDIC) and follows the grammar.\n\n## Usage\n\n### [pyknp](https://github.com/ku-nlp/pyknp) integration\n\n[pyknp](https://github.com/ku-nlp/pyknp) is the official Python binding for Jumanpp.\nInstances of [the Morpheme class](https://pyknp.readthedocs.io/en/latest/mrph.html#module-pyknp.juman.morpheme) can be used as input for Jinf.\n\n```python\nfrom jinf import Jinf\nfrom pyknp import Morpheme\n\njinf = Jinf()\n\nmrph = Morpheme(\'走る はしる 走る 動詞 2 * 0 子音動詞ラ行 10 基本形 2 "代表表記:走る/はしる"\')\n\nprint(mrph.midasi)          # 走る\nprint(mrph.genkei)          # 走る\n\nprint(jinf(mrph, "基本形"))  # 走る\nprint(jinf(mrph, "未然形"))  # 走ら\nprint(jinf(mrph, "意志形"))  # 走ろう\nprint(jinf(mrph, "命令形"))  # 走れ\n\nmrph = Morpheme(\'言語 げんご 言語 名詞 6 普通名詞 1 * 0 * 0 "代表表記:言語/げんご カテゴリ:抽象物"\')\nprint(jinf(mrph, "基本形"))  # ValueError: \'言語\' is invariable\n\nmrph = Morpheme(\'走る はしる 走る 動詞 2 * 0 子音動詞ラ行 10 基本形 2 "代表表記:走る/はしる"\')\nprint(jinf(mrph, "三角形"))  # ValueError: \'三角形\' is not a valid inflection form\n\nmrph = Morpheme(\'走る はしる 走る 動詞 2 * 0 子音動詞ラ行 10 基本形 2 "代表表記:走る/はしる"\')\nprint(jinf(mrph, "三角形"))  # ValueError: \'三角形\' is not a valid inflection form\n\nmrph = Morpheme(\'走る はしる 走る 動詞 2 * 0 子音動詞ラ行 10 基本形 2 "代表表記:走る/はしる"\')\nprint(jinf(mrph, "デアル列命令形"))  # ValueError: \'デアル列命令形\' is not a valid inflection form for \'走る\'\n```\n\n### Manual\n\nJinf also can be used by manually providing linguistic information.\n\n```python\nfrom jinf import Jinf\n\njinf = Jinf()\n\nlemma = "走る"            # corresponds to `mrph.genkei` in pyknp\ninf_type = "子音動詞ラ行"  # corresponds to `mrph.katuyou1` in pyknp\n\nprint(jinf.convert(lemma, inf_type, "基本形"))  # 走る\nprint(jinf.convert(lemma, inf_type, "未然形"))  # 走ら\nprint(jinf.convert(lemma, inf_type, "意志形"))  # 走ろう\nprint(jinf.convert(lemma, inf_type, "命令形"))  # 走れ\n```\n\n## List of inflection types/forms\n\nSee [JUMAN.katuyou](https://github.com/ku-nlp/JumanDIC/blob/master/grammar/JUMAN.katuyou) in [JumanDic](https://github.com/ku-nlp/JumanDIC).\n',
    'author': 'Hirokazu Kiyomaru',
    'author_email': 'h.kiyomaru@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hkiyomaru/jinf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
