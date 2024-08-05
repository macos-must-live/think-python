import os
import re
from collections import defaultdict
from dependencies import build_deps

class View:
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
    entity = entity.strip()
    entity = entity.replace("[", "")
    entity = entity.replace("]", "")
    entity = entity.replace("dbo.", "")
    return entity.lower()
  
  def _notApplicable(self, entity: str):
    return entity.lower() == self.name or entity.isdecimal() or entity.lower() in set([
      "", 
      "from", 
      "=", 
      "<", 
      ">", 
      ">=", 
      "<=", 
      "!=", 
      "<>", 
      "*", 
      "and", 
      "or", 
      "not", 
      "is", 
      "null", 
      "with", 
      "(nolock)", 
      "--",
      "create",
      "view",
      "as",
      "select",
      "where",
      "order",
      "by",
      "top",
      "percent",
      "distinct",
      "go",
      "set",
      "quoted_identifier",
      "ansi_nulls",
      "on",
      "off",
   ])

  def dependencies(self):
    self.deps.clear()
    # d = []
    # result = []
    if not self.from_raw: 
      return []
    
    # for match in self.deps_pattern.findall(self.from_raw):
    for match in self.deps_pattern.findall(self.body_raw):
        if not self._notApplicable(match): 
          add = self._filterNotApplicable(match)
          if add != self.name and add not in self.deps and add in views:
            self.deps.append(add)
            # d.append(add)

    # for dep in d:
    #   if dep is not self.name and dep in views:
    #     add_deps = views[dep].dependencies()
    #     if add_deps:
    #       result.extend(add_deps)

    # self.deps.extend(result)
    # result.extend(d)
    # result.append(self.name)
    # return result
    return self.deps

  def __iter__(self):
    if not self.deps:
      self.dependencies()
    # return self
    return iter(self.deps)



with open("views.sql", ) as file:
  content = file.read()


views = defaultdict()
view_content = re.compile(r"SET QUOTED_IDENTIFIER ON[\S\s]*?SET QUOTED_IDENTIFIER OFF[\s]+?GO[\s]+?SET ANSI_NULLS ON[\s]+?GO[\s]+?")
# view_name = re.compile(r"CREATE VIEW (.*) AS")
view_parse = re.compile(r"CREATE[\s]+?VIEW[\s]+?(?P<name>.*?)[\s]+AS[\S\s]*?(?P<select>SELECT[\S\s]*?)(?P<from>FROM[\S\s]*?){0,1}(?P<where>WHERE[\S\s]*?){0,1}(?P<order>ORDER[\S\s]*?){0,1}(?P<rest>GROUP[\S\s]*?){0,1}GO\n", re.IGNORECASE)

for content_match in view_content.findall(content):
  name_match = view_parse.search(content_match)
  
  v_name = name_match.group("name")
  s = name_match.group("select")
  f = name_match.group("from")
  w = name_match.group("where")
  r = name_match.group("rest")

  v = View(v_name, content_match, s, f, w, r)
  views[v.name] = v


# print(views.keys())
# result = []
for k,v in views.items():
  print(f"{v}")
  for d in v.dependencies():
    print(f"{d:>50}")
    # if d not in result:
    #   result.append(d)

  
  # if v.name not in result:
  #   result.append(v.name)
  print("-------------------------------")

result = build_deps(views)
print(f"\nordered result: (total of {len(result)})")
res_content = []
for i,vi in enumerate(result):
  if vi in views:
    print(vi)
    res_content.append(views[vi].body_raw)

os.unlink("resultin_views.sql")

with open("resultin_views.sql", "w") as file:
  file.write("\n".join(res_content))