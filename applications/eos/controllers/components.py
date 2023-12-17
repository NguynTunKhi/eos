# -*- coding: utf-8 -*-


def breadcrumb():
  items = []
  if request.vars.items:
    items = request.vars.get('items')
  title = ''
  if request.vars.title:
    title = request.vars.get('title')
  return dict(items=items, b_title=T(title))
