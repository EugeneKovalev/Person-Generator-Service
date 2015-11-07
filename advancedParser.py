import AdvancedHTMLParser
import urllib
import sexmachine.detector
from DateFormatter import DateFormatter
'''
This service creates .scs file using wiki-url
'''


class PersonGeneratorService:

    SAVE_PATH = "/home/overlord/ostis/kb/Persons/"

    def __init__(self, wiki_url):
        wiki_parser = AdvancedHTMLParser.AdvancedHTMLParser()
        wiki_parser.parseStr(urllib.urlopen(wiki_url).read())
        self.infobox = wiki_parser.getElementsByClassName('infobox')[0]
        self.system_name = None
        self.full_name = None
        self.first_name = None
        self.last_name = None
        self.gender = None
        self.image_path = None
        self.image_name = None
        self.birth_date = None
        self.death_date = None
        self.alma_mater = []
        self.occupation = []

    def get_full_name(self, infobox):
        self.full_name = infobox.getChildren()[0].getElementsByClassName('fn')[0].innerHTML
        split_full_name = self.full_name.split(' ')
        self.system_name = '_'.join(split_full_name)
        self.first_name = split_full_name[0]
        self.last_name = ' '.join(split_full_name[1:])

    def get_image(self, infobox):
        image = infobox.getElementsByClassName('image')[0]
        for image_url_container in image.getChildren():
            image_url = image_url_container.getAttribute('src')
            image_extension = image_url.split('.')[-1]
            self.image_name = self.system_name + '.' + image_extension
            self.image_path = self.SAVE_PATH + 'content/' + self.system_name + '.' + image_extension
            urllib.urlretrieve('https:' + image_url, self.image_path)

    def get_gender(self):
        self.gender = sexmachine.detector.Detector().get_gender(self.first_name)

    def get_birth_date(self, infobox):
        for _property in infobox.getChildren():
            if _property.getChildren()[0].innerHTML.startswith('Born'):
                self.birth_date = _property.getElementsByClassName('bday')[0].innerHTML
                self.birth_date = '_'.join(self.birth_date.split('-'))
                break

    def get_death_date(self, infobox):
        for _property in infobox.getChildren():
            if _property.getChildren()[0].innerHTML.startswith('Died'):
                self.death_date = _property.getElementsByClassName('dday')[0].innerHTML
                self.death_date = '_'.join(self.death_date.split('-'))
                break

    def get_alma_mater(self, infobox):
        for _property in infobox.getChildren():
            try:
                _property.getElementsByAttr('title', 'Alma mater')[0]
                for alma_mater in _property.getChildren()[1].getChildren():
                    if len(alma_mater.innerHTML) != 0:
                        self.alma_mater.append(alma_mater.innerHTML)
            except IndexError:
                pass

    def get_occupation(self, infobox):
        for _property in infobox.getChildren():
            if _property.getChildren()[0].innerHTML == ('Profession' or 'Occupation'):
                for occupation in _property.getChildren()[1].getChildren():
                    self.occupation.append(occupation.innerHTML)

    def generate_scs_file(self):
        scs_file = open(self.SAVE_PATH + self.system_name + '.scs', 'w')
        self.write_name(scs_file)
        self.write_gender(scs_file)
        if self.image_name is not None:
            self.write_person_image(scs_file)
        if self.birth_date is not None:
            self.write_birth_date(scs_file)
        if self.death_date is not None:
            self.write_death_date(scs_file)
        if len(self.alma_mater) > 0:
            self.write_alma_mater(scs_file)
        if len(self.occupation) > 0:
            self.write_occupation(scs_file)

    def write_name(self, scs_file):
        # full name generation
        scs_file.write(self.system_name + ' => nrel_main_idtf:' + '\n')
        scs_file.write('   [' + self.full_name + '](* <- lang_en;; *);;' + '\n')
        # first name generation
        scs_file.write(self.system_name + ' => nrel_first_name:' + '\n')
        scs_file.write('    name_' + self.first_name + '(*' + '\n')
        scs_file.write(2*'    ' + ' => nrel_main_idtf: [' + self.first_name + '](* <- lang_en;; *);;' + '\n')
        scs_file.write(2*'    ' + '*);;' + '\n')
        # last name generation
        scs_file.write(self.system_name + ' => nrel_surname:' + '\n')
        scs_file.write('    surname_' + self.last_name + '(*' + '\n')
        scs_file.write(2*'    ' + ' => nrel_main_idtf: [' + self.last_name + '](* <- lang_en;; *);;' + '\n')
        scs_file.write(2*'    ' + '*);;' + '\n')

    def write_person_image(self, scs_file):
        scs_file.write(self.system_name + ' <- rrel_key_sc_element:' + '\n')
        scs_file.write('    ' + self.system_name + '_Image (*' + '\n')
        scs_file.write('    ' + '=> nrel_main_idtf: [Image of ' + self.full_name + '](* <- lang_en;; *);;' + '\n')
        scs_file.write('    ' + '<-sc_statement;;' + '\n')
        scs_file.write('    ' + '<= nrel_sc_text_translation: ...' + '\n')
        scs_file.write(2*'    ' + '(*' + '\n')
        scs_file.write(2*'    ' + '->rrel_example:' + '"file://content/' + self.image_name + '"(* <-image;; *);;' + '\n')
        scs_file.write(2*'    ' + '*);;' + '\n')
        scs_file.write('*);;' + '\n')

    def write_gender(self, scs_file):
        scs_file.write(self.system_name + ' <- concept_' + self.gender + ';;' + '\n')

    def write_birth_date(self, scs_file):
        date_formatter = DateFormatter()
        split_date = self.birth_date.split('_')
        day = split_date[2]
        month = date_formatter.get_str_month(split_date[1])
        year = split_date[0]
        scs_file.write(self.system_name + ' => nrel_date_of_birth: ' + self.birth_date + '\n')
        scs_file.write('    (*' + '\n')
        scs_file.write('    [' + month + ' ' + day + ', ' + year + '](* <- lang_en;; *);;' + '\n')
        scs_file.write('    *);;' + '\n')

    def write_death_date(self, scs_file):
        date_formatter = DateFormatter()
        split_date = self.death_date.split('_')
        day = split_date[2]
        month = date_formatter.get_str_month(split_date[1])
        year = split_date[0]
        scs_file.write(self.system_name + ' => nrel_date_of_death: ' + self.death_date + '\n')
        scs_file.write('    (*' + '\n')
        scs_file.write('    [' + month + ' ' + day + ', ' + year + '](* <- lang_en;; *);;' + '\n')
        scs_file.write('    *);;' + '\n')

    def write_alma_mater(self, scs_file):
        scs_file.write(self.system_name + ' <= nrel_student: ' + '\n')
        for i in self.alma_mater:
            '_'.join(i.split(' '))
            scs_file.write('    ' + '_'.join(i.split(' ')) + '\n')
            scs_file.write(2*'    ' + '(*' + '\n')
            scs_file.write(2*'    ' + '=> nrel_main_idtf:' + '\n')
            scs_file.write(3*'    ' + '[' + i + '](* <- lang_en;; *);;' + '\n')
            scs_file.write(2*'    ' + '*);')
            if self.alma_mater.index(i) == len(self.alma_mater) - 1:
                scs_file.write(';')
            scs_file.write('\n')

    def write_occupation(self, scs_file):
        scs_file.write(self.system_name + ' <- ' + '\n')
        for i in self.occupation:
            scs_file.write('    ' + '_'.join(i.split(' ')).lower() + '\n')
            scs_file.write(2*'    ' + '(*' + '\n')
            scs_file.write(2*'    ' + '=> nrel_main_idtf:' + '\n')
            scs_file.write(3*'    ' + '[' + i.lower() + '](* <- lang_en;; *);;' + '\n')
            scs_file.write(2*'    ' + '*);')
            if self.occupation.index(i) == len(self.occupation) - 1:
                scs_file.write(';')
            scs_file.write('\n')
        pass

person = PersonGeneratorService("https://en.wikipedia.org/wiki/Kwame_Raoul")
person.get_full_name(person.infobox)
person.get_image(person.infobox)
person.get_gender()
person.get_birth_date(person.infobox)
person.get_death_date(person.infobox)
person.get_alma_mater(person.infobox)
person.get_occupation(person.infobox)
person.generate_scs_file()

