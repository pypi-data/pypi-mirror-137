#!/usr/bin/env python
#-*- coding: utf-8 -*-

### This file is part of collorg

### collorg is free software: you can redistribute it and/or modify
### it under the terms of the GNU General Public License as published by
### the Free Software Foundation, either version 3 of the License, or
### (at your option) any later version.

### This program is distributed in the hope that it will be useful,
### but WITHOUT ANY WARRANTY; without even the implied warranty of
### MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
### GNU General Public License for more details.

### You should have received a copy of the GNU General Public License
### along with this program.  If not, see <http://www.gnu.org/licenses/>.

import webbrowser
import os
import sys
from random import randint
import pydot
import copy
from collorg.templates.document_type.html import Html

def short_name(node):
    return node.split('.')[-1].capitalize()

index_html = """
<!doctype html>
<html>
  <head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <style>
      object{{max-width: 100%}}
    </style>
  </head>
  <body>
    <object class="embeded" type="image/svg+xml" data="{}.svg"></object>
  </body>
</html>
"""

class Cmd():
    def __init__(self, controller, *args):
        self.d_nodes_by_name = {}
        if not os.path.exists('doc/graph'):
            os.makedirs('doc/graph')
        cur_dir = os.path.abspath('.')
        os.chdir(controller.repos_path)
        MCluster()
        os.chdir(cur_dir)

class MCluster:
    __ctrl = Controller()
    __db = __ctrl.db
    __db_graph = __db._di_graph
    __dgraph = pydot.Dot(
        __db.name, graph_type='digraph',
        label=__db.name, href="{}.svg".format(__db.name),
        rankdir="LR", nodesetp=.75, splines="ortho")
    __dgraph.set_edge_defaults(arrowhead="vee")
    __dgraph.set_node_defaults(shape="box")
    __d_clusters = {}
    __namespaces = []
    __tables = []

    def __href_ns(self, name=""):
        href_ns = "{}.{}.svg".format(self.__db.name, name)
        return href_ns.replace('..', '.')

    def __init__(self):
        self.__add_namespaces()
        self.__add_tables()
        self.__add_links()
        self.__draw_graphs()
        webbrowser.open_new('doc/graph/index.html')

    def __draw_graphs(self):
        self.__draw_db()
        for namespace in self.__namespaces:
            self.__draw_ns_graph(namespace)
        for fqtn in self.__tables:
            self.__draw_tbl_graph(fqtn)

    def __draw_db(self):
        print("### DB")
        graph = self.__new_graph()
        d_clusters = {}
        namespaces = self.__namespaces[:]
        namespaces.reverse()
        for namespace in namespaces:
            if '.' in namespace:
                continue
            NAMESPACE = namespace.upper()
            node = pydot.Node(
                NAMESPACE, label=NAMESPACE, tooltip=NAMESPACE,
                href=self.__href_ns(namespace))
            node.set_color('#eeeeee')
            node.set_fillcolor('#eeeeee')
            node.set_style('filled')
            graph.add_node(node)
        graph.write_svg("doc/graph/{}.svg".format(self.__db.name))
        open('doc/graph/index.html', 'w').write(
            index_html.format(self.__db.name))

    def __draw_ns_graph(self, namespace):
        print("### " + namespace)
        graph = self.__new_graph()
        d_clusters = {}
        cluster = self.__d_clusters[namespace]
        old_color = self.__d_clusters[namespace].get_color()
        greenish_color = self.__get_greenish(old_color)
        cluster.set_color(greenish_color)
        cluster.set_fillcolor(greenish_color)
        d_clusters[namespace] = cluster
        graph.add_subgraph(cluster)
        nodes_names = self.__get_nodes_names(self.__d_clusters, namespace)
        for n1, n2, data in self.__db_graph.edges(data=True):
            if n1 in nodes_names or n2 in nodes_names:
                if not n1 in nodes_names:
                    self.__add_table(n1, graph, d_clusters)
                if not n2 in nodes_names:
                    self.__add_table(n2, graph, d_clusters)
                self.__add_link(graph, n1, n2, data)
        graph.write_svg('doc/graph/{}.{}.svg'.format(self.__db.name, namespace))
        cluster.set_color(old_color)
        cluster.set_fillcolor(old_color)

    def __draw_tbl_graph(self, fqtn):
        print("### " + fqtn)
        graph = self.__new_graph()
        d_clusters = {}
        self.__add_table(fqtn, graph, d_clusters, color='#ddffdd')
        nodes_names = [fqtn]
        for n1, n2, data in self.__db_graph.edges(data=True):
            if n1 == fqtn or n2 == fqtn:
                if not n1 in nodes_names:
                    self.__add_table(n1, graph, d_clusters)
                    nodes_names.append(n1)
                if not n2 in nodes_names:
                    self.__add_table(n2, graph, d_clusters)
                    nodes_names.append(n2)
                self.__add_link(graph, n1, n2, data)
        self.__draw_inh_tree(fqtn, graph, d_clusters)
        graph.write_svg('doc/graph/{}.{}.svg'.format(self.__db.name, fqtn))

    def __new_graph(self):
        __dgraph = pydot.Dot(
            self.__db.name, graph_type='digraph',
            label=self.__db.name, href=self.__href_ns(),
            rankdir="LR", nodesetp=.75, splines="ortho")
        __dgraph.set_edge_defaults(arrowhead="vee")
        __dgraph.set_node_defaults(shape="box")
        return __dgraph

    def __get_inh_namespaces(self, namespace):
        l_ns = []
        for ns in self.__namespaces:
            if ns.find(namespace) == 0:
                l_ns.append(ns)
        return l_ns

    def __get_nodes_names(self, d_clusters, namespace=None):
        l_nodes = ['collorg']
        if namespace:
            for ns in self.__get_inh_namespaces(namespace):
                for node in d_clusters[ns].get_nodes():
                    l_nodes.append(node.get_name()[1:-1])
        else:
            for cluster in d_clusters.values():
                for node in cluster.get_nodes():
                    l_nodes.append(node.get_name()[1:-1])
        return l_nodes

    def __add_namespace(self, name, graph, d_clusters):
        parent = None
        if '.' in name:
            parent_name = name.rsplit('.', 1)[0]
            if not parent_name in d_clusters:
                self.__add_namespace(parent_name, graph, d_clusters)
            parent = d_clusters[parent_name]
        cluster = pydot.Cluster(
            name.replace(".", "_"), label=name.upper(), tooltip=name,
            href=self.__href_ns(name), style='filled')
        self.set_color(cluster, parent)
        d_clusters[name] = cluster
        if parent:
            parent.add_subgraph(cluster)
        if parent is None:
            graph.add_subgraph(d_clusters[name])

    def __add_namespaces(self):
        namespaces = self.__ctrl.db.relation('collorg.core.namespace')
        namespaces.order_by(namespaces.name_)
        names = [elt.name_.value for elt in namespaces]
        self.__namespaces = names
        names.insert(0, 'collorg')
        for name in self.__namespaces:
            self.__add_namespace(name, self.__dgraph, self.__d_clusters)

    def __table_tooltip(self, fqtn):
        table = self.__ctrl.db.relation(fqtn)
        max_len = len(fqtn)
        l_fields = []
        l_pkeys = []
        for field in table._cog_fields:
            if not field.is_inherited:
                info_field = "{}{}: {}{}".format(
                    field.pkey and "[PK] " or "",
                    field.pyname, field.sql_type,
                    field.is_fkey and " -> {}({})".format(
                        field.f_table.fqtn, field.f_fieldname) or "")
                l_fields.append(info_field)
                max_len = max(max_len, len(info_field))
                if field.pkey:
                    l_pkeys.append(field.pyname)
        if l_pkeys:
            pkey_line = "PKey ({})".format(", ".join(l_pkeys))
            max_len = max(max_len, len(pkey_line))
        sep_line = "_" * max_len
        lines = [fqtn, sep_line] + l_fields
        if l_pkeys:
            lines += [sep_line, pkey_line]
        return "&#10; ".join(lines)

    def __add_table(self, fqtn, graph, d_clusters, color='white'):
        namespace, shortname = fqtn.rsplit('.', 1)
        if shortname:
            shortname = shortname.capitalize()
        if not namespace in d_clusters:
            self.__add_namespace(namespace, graph, d_clusters)
        node = pydot.Node(
            fqtn, label=shortname, tooltip=self.__table_tooltip(fqtn),
            href=self.__href_ns(fqtn))
        if shortname == 'Oid_table':
            node.set_fontcolor('red')
        node.set_color(color)
        node.set_fillcolor(color)
        node.set_style('filled')
        d_clusters[namespace].add_node(node)

    def __add_tables(self):
        tables = self.__ctrl.db.relation('collorg.core.data_type')
        tables.order_by(tables.fqtn_)
        self.__tables = [tbl.fqtn_.value for tbl in tables]
        for fqtn in self.__tables:
            self.__add_table(fqtn, self.__dgraph, self.__d_clusters)

    def __add_link(self, graph, n1, n2, data):
        for label in data['l_fields'].keys():
            label_ = "{}_".format(label)
            c1 = randint(0, 130)
            c = randint(130, 255)
            color = "#{:02X}{:02X}{:02X}".format(c1, c1, c)
            graph.add_edge(pydot.Edge(
                n1, n2, xlabel=label_, color=color, fontcolor=color))

    def __add_links(self):
        for edge in self.__db_graph.edges(data=True):
            n1, n2, data = edge
            self.__add_link(self.__dgraph, n1, n2, data)

    def __draw_inh_tree(self, fqtn, graph, dclusters):
        tbl = self.__ctrl.db.table(fqtn)
        for parent in tbl.parents_fqtns():
            if parent == fqtn:
                continue
            if parent.split('.')[-1] == 'oid_table':
                continue
            if not parent in self.__get_nodes_names(dclusters):
                self.__add_table(parent, graph, dclusters)
            graph.add_edge(pydot.Edge(
                fqtn, parent, arrowhead="onormal", color="brown", arrowsize=2))
        for child in tbl.children_fqtns():
            if child == fqtn:
                continue
            if not child in self.__get_nodes_names(dclusters):
                self.__add_table(child, graph, dclusters)
            graph.add_edge(pydot.Edge(
                child, fqtn, arrowhead="onormal", color="brown", arrowsize=2))

    def set_color(self, cluster, parent=None):
        color = '#eeeeee'
        if parent:
            color = self.__get_darker(parent.get_color())
        cluster.set_color(color)
        cluster.set_fillcolor(color)

    def __darker(self, value):
        shades = ['ff', 'ee', 'dd', 'cc', 'bb', 'aa', '99', '88',
                  '77', '66', '55', '44', '33', '22', '11', '00']
        if value == '00':
            return '00'
        return shades[shades.index(value) + 1]

    def __get_greenish(self, color):
        R = color[1:3]
        G = color[3:5]
        B = color[5:7]
        return '#{}{}{}'.format(self.__darker(R), G, self.__darker(B))

    def __get_darker(self, color):
        R = color[1:3]
        G = color[3:5]
        B = color[5:7]
        return '#{}{}{}'.format(
            self.__darker(R), self.__darker(G), self.__darker(B))

if __name__ == '__main__':
    MCluster()
