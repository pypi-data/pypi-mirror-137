"""Plotting class."""
# -*- coding: utf-8 -*-
# @Author: AnthonyKenny98
# @Date:   2021-11-20 14:52:11
# @Last Modified by:   AnthonyKenny98
# @Last Modified time: 2021-11-20 15:04:09

import os
import json
import datetime


class Thinkcell():
    """Thinkcell Plot class."""

    template_dir = 'https://eyaustralia.sharepoint.com/sites/EYPJPTeam/Shared%20Documents/Analytics/thinkcell-templates/'

    def __init__(self, categories, data, title, plot_type, units):
        """Initialise."""
        self.categories = categories
        self.data = dict(sorted(data.items(), key=lambda item: item[1][0], reverse=True))
        self.title = title.upper()
        self.plot_type = plot_type
        self.units=units

    def quick_plot(self, out_dir='./'):
        template_name = self.template_dir + self.plot_type + '.pptx'
        template_chart_ref = 'template_chart'
        template_title_ref = 'template_title'
        template_subtitle_ref = 'template_subtitle'

        out_dir += '' if out_dir.endswith('/') else '/'
        filepath = out_dir + self.title + '_' + self.plot_type + '.ppttc'

        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        tc = PPTTC(out_file = filepath)
        template = tc.add_template(template_name)

        template.update_textfield(
            field_name=template_title_ref,
            text=self.title)
        template.update_textfield(
            field_name=template_subtitle_ref,
            text=self.units)
        template.update_chart(
            chart_name=template_chart_ref,
            categories=self.categories,
            data=self.data)

        print("Saving to: " + filepath)
        tc.save()

        return filepath


class PPTTC():

    def __init__(self, out_file=None, update=False):
        self.templates = []
        if out_file is not None:
            out_file += '.ppttc' if out_file[-6:] != '.ppttc' else ''
        self.out_file = out_file
        if os.path.exists(out_file) and update == True:
            self.load_ppttc(out_file)

    def load_ppttc(self, target):
        if target is None:
            self.target = None

        # TODO - check target exists
        with open(target) as f:
            target_templates = json.load(f)

        # Parse target json
        self.templates += [Template(template_ref=t['template'], data=t['data'])for t in target_templates]


    def add_template(self, template_ref):
        template = Template(template_ref)
        self.templates.append(template)
        return template

    def update_template(self, template_ref):
        template = [t for t in self.templates if t.template == template_ref]
        template = template[0] if len(template) else self.add_template(template_ref)
        return template

    def save(self):

        out_file = open(self.out_file, 'w')
        json.dump([
            {'template': t.template, 'data': 
                [{'name': o.name, 'table': o.table} for o in t.data]
            } for t in self.templates], out_file)
        out_file.close()


class Template():

    def __init__(self, template_ref, data = [], name=None):
        self.template = template_ref
        self.data = []
        for obj in data:
            obj_type = TextField if len(obj['table']) == 1 else Chart
            self.data.append(obj_type(obj['name'], obj['table']))

    def update_object(self, name, data, obj_type):
        # Find object if it already exists in data, else create new object
        find_obj = [obj for obj in self.data if obj.name == name]
        if len(find_obj):
            obj = find_obj[0]
        else:
            obj = obj_type(name)
            self.data.append(obj)
        obj.update(data)


    def update_textfield(self, field_name, text):

        self.update_object(field_name, text, TextField)

    def update_chart(self, chart_name, categories, data):

        data = {'categories': categories, 'series': data}
        self.update_object(chart_name, data, Chart)

class Object():

    def __init__(self, name, data=None):
        self.name = name
        self.table = None
        if data is not None:
            self.load(data)

    def load(self, data):
        pass

    def update(self, data):
        pass

    def non_numeric_kv(self, item):

        type_select = {
            str: 'string',
            datetime.date: 'date'
        }

        return {type_select[type(item)]: str(item)}

class TextField(Object):

    def __init__(self, name, data=None):
        super().__init__(name, data)

    def __repr(self):
        return json.dumps(self.__dict__)

    def load(self, data):
        self.table = data

    def update(self, data):
        self.table = [[self.non_numeric_kv(data)]]

class Chart(Object):

    def __init__(self, name, data=None):
        super().__init__(name, data)

    def load(self, data):
        self.table = data

    def update(self, data):
        
        # Setup blank table
        self.table = []

        # First row - Blank cell followed by category labels
        self.table.append(
            [None] + [self.non_numeric_kv(cat) for cat in data['categories']])
        
        # Second row - 100% values (blank row for now)
        self.table.append([])

        # Following rows - each data series
        for key, vals in data['series'].items():
            self.table.append(
                [self.non_numeric_kv(key)] + [{'number':val} for val in vals])
