file="data/05_data.txt"

rules=[]
prev_rules={}
post_rules={}
pages=[]
valid_pages=[]
sum_mid_page=0
sum_mid_page_bad=0

def valid_rule(pages, prev_rules, post_rules)->bool:
  for i in range(len(pages)):
    page1=pages[i]
    for j in range(i,len(pages)):
      page2=pages[j]
      if page2 in prev_rules and page1 in prev_rules[page2]: return False
      if page1 in post_rules and page2 in post_rules[page1]: return False
  return True

def rearrange_pages(pages, prev_rules, post_rules)->list:
  new_pages=[]
  for i in range(len(pages)):
    page=pages[i]
    if i==0: new_pages.append(page)
    else:
      new_position=0
      for j in range(len(new_pages)):
        new_page=new_pages[j]
        if page in prev_rules and new_page in prev_rules[page]:
          new_position=j
          break
        if page in post_rules and new_page in post_rules[page]: new_position=j+1
      new_pages.insert(new_position, page)
  return new_pages

def get_mid_page(pages)->int:
  length=len(pages)
  mig_length=int(length/2)
  return int(pages[mig_length])

with open(file, "r") as f:
  seccio_norma=True
  for linia in f:
    linia = linia.strip()
    if linia == "":
      seccio_norma=False
      continue
    if seccio_norma:
      nova_norma=linia.split("|")
      rules.append(nova_norma)
      if nova_norma[0] not in prev_rules:
        prev_rules[nova_norma[0]]=[]
      if nova_norma[1] not in post_rules:
        post_rules[nova_norma[1]]=[]
      prev_rules[nova_norma[0]].append(nova_norma[1])
      post_rules[nova_norma[1]].append(nova_norma[0])
    else:
      pages.append(linia.split(","))

for page in pages:
  if valid_rule(page, prev_rules, post_rules):
    valid_pages.append(page)
    sum_mid_page+=get_mid_page(page)
  else:
    new_page=rearrange_pages(page, prev_rules, post_rules)
    sum_mid_page_bad+=get_mid_page(new_page)

print("EL valor de la suma de la pàgina central de norma vàlides és:", sum_mid_page) # 6949
print("El valor de la suma de la pàgina central de normes reordenades és:", sum_mid_page_bad) # 4145