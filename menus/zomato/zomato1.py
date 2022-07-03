from chompjs import parse_js_object
script = """__DATA__ = {"data":{"type":"@products", "products":[{"id":12345678, "name":"Bacon", "brand": "Some Brand", "price":2.50, "instock": false},{"id":12345679, "name":"Ham", "price":3.50, "instock": true},{"id":12345680, "name":"Beef", "price":1.50, "instock": false}]}};
some_javascript(data) {results = do_stuff(data); return results};
new beep_boop_js_var = some_javascript(__DATA__)"""

data = parse_js_object(script)
data = data['data']['products']
for i in data:
   print(i['name'])
