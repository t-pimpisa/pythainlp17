# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from collections import Counter
import unittest
import sys

from pythainlp.change import texttoeng, texttothai
from pythainlp.collation import collation
from pythainlp.corpus import (
    alphabet,
    country,
    newthaiword,
    provinces,
    stopwords,
    thaiword,
    tone,
    wordnet,
)
from pythainlp.date import now, reign_year_to_ad
from pythainlp.keywords import find_keyword
from pythainlp.MetaSound import MetaSound
from pythainlp.ner import thainer
from pythainlp.number import numtowords
from pythainlp.rank import rank
from pythainlp.romanization import romanization
from pythainlp.soundex import LK82, Udom83
from pythainlp.spell import spell
from pythainlp.summarize import summarize_text
from pythainlp.tag import pos_tag, pos_tag_sents
from pythainlp.tokenize import (
    etcc,
    isthai,
    syllable_tokenize,
    tcc,
    word_tokenize,
)
from pythainlp.util import listtext_num2num, normalize


class TestUM(unittest.TestCase):
    """
    ระบบทดสอบการทำงานของโค้ดของ PyThaiNLP 1.7
    """
    def test_segment(self):
        self.assertEqual(
            word_tokenize('ฉันรักภาษาไทยเพราะฉันเป็นคนไทย'),
            [u'ฉัน', u'รัก', u'ภาษาไทย', u'เพราะ', u'ฉัน', u'เป็น', u'คนไทย']
        )

    def test_syllable_tokenize(self):
        self.assertEqual(
            syllable_tokenize("สวัสดีชาวโลก"),
            [u'สวัส', u'ดี', u'ชาว', u'โลก']
        )

    def test_segment_icu(self):
        self.assertEqual(
            word_tokenize('ฉันรักภาษาไทยเพราะฉันเป็นคนไทย', engine='icu'),
            [
                u'ฉัน',
                u'รัก',
                u'ภาษา',
                u'ไทย',
                u'เพราะ',
                u'ฉัน',
                u'เป็น',
                u'คน',
                u'ไทย',
            ]
        )

    def test_segment_mm(self):
        self.assertEqual(
            word_tokenize('ฉันรักภาษาไทยเพราะฉันเป็นคนไทย', engine='mm'),
            [u'ฉัน', u'รัก', u'ภาษาไทย', u'เพราะ', u'ฉัน', u'เป็น', u'คนไทย']
        )

    def test_segment_newmm(self):
        self.assertEqual(
            word_tokenize('ฉันรักภาษาไทยเพราะฉันเป็นคนไทย', engine='newmm'),
            [u'ฉัน', u'รัก', u'ภาษาไทย', u'เพราะ', u'ฉัน', u'เป็น', u'คนไทย']
        )
        self.assertEqual(
            word_tokenize('สวัสดีครับ สบายดีไหมครับ', engine='newmm'),
            [u'สวัสดี', u'ครับ', u' ', u'สบายดี', u'ไหม', u'ครับ']
        )
        self.assertEqual(
            word_tokenize('จุ๋มง่วงนอนยัง', engine='newmm'),
            [u'จุ๋ม', u'ง่วงนอน', u'ยัง']
        )
        self.assertEqual(
            word_tokenize('จุ๋มง่วง', engine='newmm'),
            [u'จุ๋ม', u'ง่วง']
        )
        self.assertEqual(
            word_tokenize('จุ๋ม   ง่วง', engine='newmm', whitespaces=False),
            [u'จุ๋ม', u'ง่วง']
        )

    def test_segment_longest_matching(self):
        self.assertEqual(
            word_tokenize(
                'ฉันรักภาษาไทยเพราะฉันเป็นคนไทย',
                engine='longest-matching'
            ),
            [u'ฉัน', u'รัก', u'ภาษาไทย', u'เพราะ', u'ฉัน', u'เป็น', u'คนไทย']
        )

    def test_segment_wordcut(self):
        if (sys.version_info >= (3, 4) and
                sys.platform != 'win32' and
                sys.platform != 'win64'):
            self.assertEqual(
                word_tokenize(
                    'ฉันรักภาษาไทยเพราะฉันเป็นคนไทย',
                    engine='wordcutpy'
                ),
                [
                    u'ฉัน',
                    u'รัก',
                    u'ภาษา',
                    u'ไทย',
                    u'เพราะ',
                    u'ฉัน',
                    u'เป็น',
                    u'คน',
                    u'ไทย',
                ]
            )

    def test_rank(self):
        self.assertEqual(
            rank(["แมว", "คน", "แมว"]),
            Counter({'แมว': 2, 'คน': 1})
        )

    def test_change(self):
        self.assertEqual(texttothai('l;ylfu8iy['), 'สวัสดีครับ')
        self.assertEqual(texttoeng('สวัสดีครับ'), 'l;ylfu8iy[')

    def test_romanization(self):
        self.assertEqual(romanization('แมว'), 'maeo')
        self.assertEqual(romanization('แมว', 'pyicu'), 'mæw')

    def test_romanization_royin(self):
        engine = 'royin'
        self.assertEqual(romanization('แมว', engine=engine), 'maeo')
        self.assertEqual(romanization('เดือน', engine=engine), 'duean')
        self.assertEqual(romanization('ดู', engine=engine), 'du')
        self.assertEqual(romanization('ดำ', engine=engine), 'dam')
        self.assertEqual(romanization('บัว', engine=engine), 'bua')

    def test_number(self):
        self.assertEqual(
            numtowords(5611116.50),
            'ห้าล้านหกแสนหนึ่งหมื่นหนึ่งพันหนึ่งร้อยสิบหกบาทห้าสิบสตางค์'
        )

    def test_tcc(self):
        self.assertEqual(tcc.tcc('ประเทศไทย'), 'ป/ระ/เท/ศ/ไท/ย')

    def test_isthai(self):
        self.assertEqual(isthai('ประเทศไทย'), {'thai': 100.0})

    # def test_WhitespaceTokenizer(self):
    #     self.assertEqual(WhitespaceTokenizer("1 2 3"),['1', '2', '3'])

    def test_etcc(self):
        self.assertEqual(etcc.etcc('คืนความสุข'), '/คืน/ความสุข')

    def test_lk82(self):
        self.assertEqual(LK82('รถ'), 'ร3000')
        self.assertEqual(Udom83('รถ'), 'ร800000')

    def test_ms(self):
        self.assertEqual(MetaSound('คน'), '15')

    def test_wordnet(self):
        self.assertEqual(
            wordnet.synset('spy.n.01').lemma_names('tha'),
            ['สปาย', 'สายลับ']
        )
        self.assertIsNotNone(wordnet.langs())

    def test_stopword(self):
        self.assertIsNotNone(stopwords.words('thai'))

    def test_spell(self):
        self.assertIsNotNone(spell('เน้ร'))

    def test_date(self):
        self.assertIsNotNone(now())
        self.assertEqual(reign_year_to_ad(2, 10), 2017)

    def test_summarize(self):
        text = 'อาหาร หมายถึง ของแข็งหรือของเหลว '
        text += 'ที่กินหรือดื่มเข้าสู่ร่างกายแล้ว '
        text += 'จะทำให้เกิดพลังงานและความร้อนแก่ร่างกาย '
        text += 'ทำให้ร่างกายเจริญเติบโต '
        text += 'ซ่อมแซมส่วนที่สึกหรอ ควบคุมการเปลี่ยนแปลงต่างๆ ในร่างกาย '
        text += 'ช่วยทำให้อวัยวะต่างๆ ทำงานได้อย่างปกติ '
        text += 'อาหารจะต้องไม่มีพิษและไม่เกิดโทษต่อร่างกาย'
        self.assertEqual(
            summarize_text(text=text, n=1, engine='frequency'),
            [u'อาหารจะต้องไม่มีพิษและไม่เกิดโทษต่อร่างกาย']
        )

    def test_corpus(self):
        self.assertIsNotNone(alphabet.get_data())
        self.assertIsNotNone(country.get_data())
        self.assertIsNotNone(tone.get_data())
        self.assertIsNotNone(provinces.get_data())
        self.assertTrue(len(newthaiword.get_data()) > len(thaiword.get_data()))

    def test_collation(self):
        self.assertEqual(collation(['ไก่', 'กก']), [u'กก', u'ไก่'])
        self.assertEqual(
            collation(['ไก่', 'เป็ด', 'หมู', 'วัว']),
            [u'ไก่', u'เป็ด', u'วัว', u'หมู']
        )

    def test_normalize(self):
        self.assertEqual(normalize('เเปลก'), 'แปลก')

    def test_listtext_num2num(self):
        if sys.version_info >= (3, 4):
            self.assertEqual(
                listtext_num2num(
                    [
                        u'หก',
                        u'ล้าน',
                        u'หกแสน',
                        u'หกหมื่น',
                        u'หกพัน',
                        u'หกร้อย',
                        u'หกสิบ',
                        u'หก',
                    ]
                ),
                6666666
            )

    def test_keywords(self):
        word_list = word_tokenize(
            'แมวกินปลาอร่อยรู้ไหมว่าแมวเป็นแมวรู้ไหมนะแมว',
            engine='newmm'
        )
        self.assertEqual(find_keyword(word_list), {u'แมว': 4})

    def test_tag(self):
        self.assertEqual(
            pos_tag(word_tokenize('คุณกำลังประชุม'), engine='old'),
            [('คุณ', 'PPRS'), ('กำลัง', 'XVBM'), ('ประชุม', 'VACT')]
        )
        self.assertEqual(
            pos_tag_sents([['ผม', 'กิน', 'ข้าว'], ['แมว', 'วิ่ง']]),
            [
                [('ผม', 'PPRS'), ('กิน', 'VACT'), ('ข้าว', 'NCMN')],
                [('แมว', 'NCMN'), ('วิ่ง', 'VACT')],
            ]
        )

        if sys.version_info >= (3, 4):
            self.assertEqual(
                str(type(pos_tag(
                    word_tokenize('ผมรักคุณ'),
                    engine='artagger'
                ))),
                "<class 'list'>"
            )

    def test_ner(self):
        ner = thainer()
        self.assertEqual(
            ner.get_ner('แมวทำอะไรตอนห้าโมงเช้า'),
            [
                ('แมว', 'NCMN', 'O'),
                ('ทำ', 'VACT', 'O'),
                ('อะไร', 'PNTR', 'O'),
                ('ตอน', 'NCMN', 'O'),
                ('ห้า', 'VSTA', 'B-TIME'),
                ('โมง', 'NCMN', 'I-TIME'),
                ('เช้า', 'ADVN', 'I-TIME'),
            ]
        )
        self.assertEqual(
            ner.get_ner('แมวทำอะไรตอนห้าโมงเช้า', postag=False),
            [
                ('แมว', 'O'),
                ('ทำ', 'O'),
                ('อะไร', 'O'),
                ('ตอน', 'O'),
                ('ห้า', 'B-TIME'),
                ('โมง', 'I-TIME'),
                ('เช้า', 'I-TIME'),
            ]
        )


if __name__ == '__main__':
    unittest.main()
