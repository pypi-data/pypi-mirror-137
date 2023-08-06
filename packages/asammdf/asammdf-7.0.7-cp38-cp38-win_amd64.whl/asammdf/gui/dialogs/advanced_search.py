# -*- coding: utf-8 -*-
import re

from natsort import natsorted
from PyQt5 import QtCore, QtWidgets

from ...blocks.utils import extract_cncomment_xml
from ..ui import resource_rc as resource_rc
from ..ui.search_dialog import Ui_SearchDialog
from .range_editor import RangeEditor


class AdvancedSearch(Ui_SearchDialog, QtWidgets.QDialog):
    def __init__(
        self,
        mdf,
        return_names=False,
        show_add_window=False,
        show_apply=False,
        show_pattern=True,
        apply_text="Apply",
        add_window_text="Add window",
        show_search=True,
        window_title="Search & select channels",
        pattern=None,
        *args,
        **kwargs,
    ):

        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.selection.all_texts = True

        self.result = {}
        self.add_window_request = False
        self.channels_db = mdf.channels_db
        self.mdf = mdf

        self.apply_btn.clicked.connect(self._apply)
        self.add_btn.clicked.connect(self._add)
        self.add_window_btn.clicked.connect(self._add_window)
        self.cancel_btn.clicked.connect(self._cancel)

        self.search_box.editingFinished.connect(self.search_text_changed)
        self.match_kind.currentTextChanged.connect(self.search_box.textChanged.emit)
        self.matches.itemDoubleClicked.connect(self._match_double_clicked)
        self.selection.itemDoubleClicked.connect(self._selection_double_clicked)

        self.matches.header().sectionResized.connect(self.section_resized)
        self.selection.header().sectionResized.connect(self.section_resized)

        self.apply_pattern_btn.clicked.connect(self._apply_pattern)
        self.cancel_pattern_btn.clicked.connect(self._cancel_pattern)
        self.define_ranges_btn.clicked.connect(self._define_ranges)

        self.search_box.setFocus()

        self._return_names = return_names
        self.ranges = []

        self.pattern_window = False

        self.apply_btn.setText(apply_text)
        self.add_window_btn.setText(add_window_text)

        self.selection.can_delete_items = True
        self.matches.can_delete_items = False

        if not show_add_window:
            self.add_window_btn.hide()

        if not show_apply:
            self.apply_btn.hide()

        if not show_pattern:
            self.tabs.removeTab(1)

        if not show_search:
            self.tabs.removeTab(0)

        if pattern:
            self.pattern.setText(pattern["pattern"])
            self.filter_type.setCurrentText(pattern["filter_type"])
            self.filter_value.setValue(pattern["filter_value"])
            self.pattern_match_type.setCurrentText(pattern["match_type"])
            self.raw.setCheckState(
                QtCore.Qt.Checked if pattern["raw"] else QtCore.Qt.Unchecked
            )
            self.name.setText(pattern["name"])
            self.ranges = pattern["ranges"]

        self.setWindowTitle(window_title)

        self.matches.setColumnWidth(0, 450)
        self.matches.setColumnWidth(1, 40)
        self.matches.setColumnWidth(2, 40)
        self.matches.setColumnWidth(3, 170)
        self.matches.setColumnWidth(4, 170)

    def search_text_changed(self):
        text = self.search_box.text().strip()
        if len(text) >= 2:
            if self.match_kind.currentText() == "Wildcard":
                pattern = text.replace("*", "_WILDCARD_")
                pattern = re.escape(pattern)
                pattern = pattern.replace("_WILDCARD_", ".*")
            else:
                pattern = text

            try:
                pattern = re.compile(f"(?i){pattern}")
                found_names = [
                    name for name in self.channels_db if pattern.fullmatch(name)
                ]

                matches = {}
                for name in found_names:
                    for entry in self.channels_db[name]:

                        if entry not in matches:
                            (group_index, channel_index) = entry
                            ch = self.mdf.groups[group_index].channels[channel_index]
                            cg = self.mdf.groups[group_index].channel_group

                            source = ch.source or cg.acq_source

                            matches[entry] = {
                                "names": [],
                                "comment": extract_cncomment_xml(ch.comment).strip(),
                                "source_name": source.name if source else "",
                                "source_path": source.path if source else "",
                            }

                        info = matches[entry]

                        if name == ch.name:
                            info["names"].insert(0, name)
                        else:
                            info["names"].append(name)

                matches = [
                    (group_index, channel_index, info)
                    for (group_index, channel_index), info in matches.items()
                ]
                matches.sort(key=lambda x: info["names"][0])

                self.matches.clear()
                for group_index, channel_index, info in matches:
                    names = info["names"]
                    group_index, channel_index = str(group_index), str(channel_index)
                    item = QtWidgets.QTreeWidgetItem(
                        [
                            names[0],
                            group_index,
                            channel_index,
                            info["source_name"],
                            info["source_path"],
                            info["comment"],
                        ]
                    )
                    self.matches.addTopLevelItem(item)

                    children = [
                        QtWidgets.QTreeWidgetItem(
                            [
                                name,
                                group_index,
                                channel_index,
                                info["source_name"],
                                info["source_path"],
                                info["comment"],
                            ]
                        )
                        for name in names[1:]
                    ]

                    if children:
                        item.addChildren(children)

                if matches:
                    self.status.setText(f"{len(found_names)} results")
                else:
                    self.status.setText("No results")

                self.matches.expandAll()

            except Exception as err:
                self.status.setText(str(err))
                self.matches.clear()

    def _add(self, event):
        selection = set()

        iterator = QtWidgets.QTreeWidgetItemIterator(self.selection)
        while iterator.value():
            item = iterator.value()
            data = (
                item.text(0),
                item.text(1),
                item.text(2),
                item.text(3),
                item.text(4),
                item.text(5),
            )
            selection.add(data)

            iterator += 1

        for item in self.matches.selectedItems():
            data = (
                item.text(0),
                item.text(1),
                item.text(2),
                item.text(3),
                item.text(4),
                item.text(5),
            )
            selection.add(data)

        selection = natsorted(selection)

        items = [QtWidgets.QTreeWidgetItem(texts) for texts in selection]

        self.selection.clear()
        self.selection.addTopLevelItems(items)

    def _apply(self, event=None):
        if self._return_names:
            self.result = set()

            iterator = QtWidgets.QTreeWidgetItemIterator(self.selection)
            while iterator.value():
                item = iterator.value()
                self.result.add(item.text(0))
                iterator += 1
        else:
            self.result = {}

            iterator = QtWidgets.QTreeWidgetItemIterator(self.selection)
            while iterator.value():
                item = iterator.value()

                entry = int(item.text(1)), int(item.text(2))
                name = item.text(0)
                self.result[entry] = name
                iterator += 1

        self.close()

    def _apply_pattern(self, event):
        self.result = {
            "pattern": self.pattern.text().strip(),
            "match_type": self.pattern_match_type.currentText(),
            "filter_type": self.filter_type.currentText(),
            "filter_value": self.filter_value.value(),
            "raw": self.raw.checkState() == QtCore.Qt.Checked,
            "ranges": self.ranges,
            "name": self.name.text().strip(),
        }

        if not self.result["pattern"]:
            QtWidgets.QMessageBox.warning(
                self, "Cannot apply pattern", "The pattern cannot be empty"
            )
            return

        if not self.result["name"]:
            QtWidgets.QMessageBox.warning(
                self, "Cannot apply pattern", "The name cannot be empty"
            )
            return

        self.pattern_window = True
        self.close()

    def _add_window(self, event=None):
        self.add_window_request = True
        self._apply()

    def _cancel(self, event):
        self.result = {}
        self.close()

    def _cancel_pattern(self, event):
        self.result = {}
        self.close()

    def _define_ranges(self, event=None):
        name = self.pattern.text().strip()
        dlg = RangeEditor(f"Channel of <{name}>", ranges=self.ranges, parent=self)
        dlg.exec_()
        if dlg.pressed_button == "apply":
            self.ranges = dlg.result

    def _match_double_clicked(self, item):
        selection = set()
        new_item = item

        iterator = QtWidgets.QTreeWidgetItemIterator(self.selection)
        while iterator.value():
            item = iterator.value()
            data = (
                item.text(0),
                item.text(1),
                item.text(2),
                item.text(3),
                item.text(4),
                item.text(5),
            )
            selection.add(data)

            iterator += 1

        new_data = (
            new_item.text(0),
            new_item.text(1),
            new_item.text(2),
            new_item.text(3),
            new_item.text(4),
            new_item.text(5),
        )

        if new_data not in selection:
            selection.add(new_data)

            selection = natsorted(selection)

            items = [QtWidgets.QTreeWidgetItem(texts) for texts in selection]

            self.selection.clear()
            self.selection.addTopLevelItems(items)

    def _selection_double_clicked(self, item):
        root = self.selection.invisibleRootItem()
        (item.parent() or root).removeChild(item)

    def section_resized(self, index, old_size, new_size):
        self.selection.setColumnWidth(index, new_size)
        self.matches.setColumnWidth(index, new_size)
