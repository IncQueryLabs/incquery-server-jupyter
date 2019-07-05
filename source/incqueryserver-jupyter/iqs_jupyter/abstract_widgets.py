# Copyright 2019 IncQuery Labs Ltd.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#  http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from ipywidgets.widgets.widget import Widget

'''
Created on 2019. júl. 4.

@author: Gabor Bergmann
'''

from abc import ABC, abstractmethod
from typing import Dict, Tuple, Any, Hashable, List

import ipywidgets as widgets
from IPython.display import display

class AbstractElementInfoWidget(ABC):
    def __init__(
        self,
        #initial_element,
        attempt_batch_prefetch = True,
        grid_container_layout = widgets.Layout(
            grid_template_columns = "25% 73%", 
            grid_gap="2%"),
        field_box_layout = widgets.Layout(
            overflow_x='auto', 
            justify_content='flex-end'),
        slot_item_layout = widgets.Layout(
            width='auto', 
            flex='0 0 auto'),
        slot_box_layout = widgets.Layout(
            overflow_x='auto',
            #border='solid',
            width='auto',
            height='',
            flex_flow='row',
            display='flex', 
            justify_content='flex-start')
    ):
        self.attempt_batch_prefetch = attempt_batch_prefetch
        self.grid_container_layout = grid_container_layout
        self.field_box_layout = field_box_layout
        self.slot_item_layout = slot_item_layout
        self.slot_box_layout = slot_box_layout
        self.accordion = widgets.Accordion()
        self.element_list = []
        self.element_id_to_index = {}
        #self.initial_element = initial_element
        #self.show_element_pane(initial_element)
     
    @abstractmethod
    def _to_hashable_identifier(self, element) -> Hashable:
        pass
    
    @abstractmethod
    def _to_field_display_name(self, element, field) -> str:
        pass
    
    @abstractmethod
    def _unpack_element(self, element) -> Tuple[str, Dict[str, Any]]:
        pass
    
    @abstractmethod
    def _do_retrieve_batch(self, element, field_values):
        pass
    
    @abstractmethod
    def _value_widget_list(self, element, field, value) -> List[Widget]:
        pass
        
    def _add_element_pane(self, element):
        header, field_values = self._unpack_element(element)

        if self.attempt_batch_prefetch:
            self._do_retrieve_batch(element, field_values)
            
        import html
        grid_content_boxes = []
        for field,value in field_values.items():
            field_display_name = self._to_field_display_name(element, field)
            if field_display_name and (value is not None) and not ([]==value):
                field_widget = widgets.HTML(value = "<b>{}</b>".format(html.escape(field_display_name)))
                field_box = widgets.Box(children=[field_widget], layout=self.field_box_layout)
                slot_widget_list = self._value_widget_list(element, field, value)
                slot_box = widgets.Box(children=slot_widget_list, layout=self.slot_box_layout)
                grid_content_boxes.extend([field_box, slot_box])
        content = widgets.GridBox(layout=self.grid_container_layout, children=grid_content_boxes)
        
        self.accordion.children = list(self.accordion.children) + [content]
        self.accordion.set_title(len(self.element_list), header)
        self.element_id_to_index[self._to_hashable_identifier(element)] = len(self.element_list)
        self.element_list.append(element)


    def _create_value_widget_attribute(self, value):
        # TODO handle data types separately, e.g. checkbox for boolean
        value_str = value if isinstance(value, str) else str(value)
        return widgets.Label(value=value_str, layout=self.slot_item_layout)
    def _create_value_widget_reference(self, referred_element, short_text, long_text):
        button = widgets.Button(
            description=short_text,
            #disabled=False,
            button_style='info', # 'primary', 'success', 'info', 'warning', 'danger' or ''
            #icon='check',
            tooltip=long_text,
            layout=self.slot_item_layout
        )
        button.on_click(lambda b: self.show_element_pane(referred_element))
        return button


    def show_element_pane(self, element, highlight=True):
        element_id = self._to_hashable_identifier(element)
        if element_id not in self.element_id_to_index:
            self._add_element_pane(element)
        if highlight:
            self.accordion.selected_index = self.element_id_to_index[element_id]
        
    def selected_element(self):
        if self.accordion.selected_index is None:
            return None
        else:
            return self.element_list[self.accordion.selected_index]

    def _repr_html_(self):
        self.display()    
          
    def display(self):
        display(self.accordion)
