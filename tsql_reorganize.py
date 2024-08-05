import os
import re
from collections import defaultdict

class View(object):
  def __init__(self, n, b, s, f, w, r) -> None:
    self.name = self._filterNotApplicable(n)
    self.body_raw = b
    self.select_raw = s
    self.from_raw = f
    self.where_raw = w
    self.rest_raw = r
    self.deps_pattern = re.compile(r"(\S+)", re.IGNORECASE)
    self.deps = []

  def __str__(self) -> str:
    return self.name
  
  def _filterNotApplicable(self, entity: str):
    entity = entity.replace("[", "")
    entity = entity.replace("]", "")
    entity = entity.replace("dbo.", "")
    return entity.lower()
  
  def _notApplicable(self, entity: str):
    return entity.isdecimal() or entity.lower() in ["", "from", "=", ">", ">", ">=", "<=", "!=", "<>", "and", "or", "not", "is", "null", "with", "(nolock)", "--"]
  
  def dependencies(self):
    # self.deps.clear()
    d = []
    result = []
    if not self.from_raw: 
      return result
    
    for match in self.deps_pattern.findall(self.from_raw):
        if not self._notApplicable(match): 
          add = self._filterNotApplicable(match)
          if add not in d and add in views:
            d.append(add)

    for dep in d:
      if dep is not self.name and dep in views:
        add_deps = views[dep].dependencies()
        if add_deps:
          result.extend(add_deps)

    # self.deps.extend(result)
    result.extend(d)
    # result.append(self.name)
    return result
  




with open("views.sql", ) as file:
  content = file.read()


views = defaultdict()
view_content = re.compile(r"SET QUOTED_IDENTIFIER ON[\S\s]*?SET QUOTED_IDENTIFIER OFF[\s]+?GO[\s]+?SET ANSI_NULLS ON[\s]+?GO[\s]+?")
# view_name = re.compile(r"CREATE VIEW (.*) AS")
view_name = re.compile(r"CREATE[\s]+?VIEW[\s]+?(?P<name>.*?)[\s]+AS[\S\s]*?(?P<select>SELECT[\S\s]*?)(?P<from>FROM[\S\s]*?){0,1}(?P<where>WHERE[\S\s]*?){0,1}(?P<order>ORDER[\S\s]*?){0,1}(?P<rest>GROUP[\S\s]*?){0,1}GO\n", re.IGNORECASE)

for content_match in view_content.findall(content):
  name_match = view_name.search(content_match)
  
  v_name = name_match.group("name")
  select = name_match.group("select")
  f = name_match.group("from")
  w = name_match.group("where")
  r = name_match.group("rest")

  v = View(v_name, content_match, select, f, w, r)
  views[v.name] = v

# print(views.keys())
result = []
for k,v in views.items():
  for d in v.dependencies():
    print(d)
    if d not in result:
      result.append(d)

  print(f"--{v}")
  if v.name not in result:
    result.append(v.name)
  print("-------------------------------")

res_content = []
for i in result:
  if i in views:
    res_content.append(views[i].body_raw)

os.unlink("resultin_views.sql")

with open("resultin_views.sql", "w") as file:
  file.write("\n".join(res_content))