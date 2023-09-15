import fastapi
from fastapi import FastAPI, Path, Query, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    brand: str 
    
class UpdateItem(BaseModel):
    name: str = None
    price: float = None
    brand: str = None

inventory = {}


## /item Endpoint (GET, POST, PUT, DELETE)
@app.get("/item/{item_id}")
def get_item(item_id: int = Path(description="Get item details by item_id",ge=1)):
    if item_id not in inventory:
        raise HTTPException(404, "Item ID does not exist")
    return inventory[item_id]
@app.post("/item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(400,detail="Item ID already exists")
    inventory[item_id] = item
    return inventory[item_id]
@app.put("/item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    #Item class requires name, price, and brand. 
    #But if only one of the fields requires an update, we will only supply that field
    #in the request body of the PUT request. This would throw an error as all 3 fields
    #are required. To workaround this, we create another class UpdateItem and set its
    #fields to optional.
    
    if item_id not in inventory:
        raise HTTPException(404, detail= "Item ID does not exist.")
    if item.name != None:
        inventory[item_id].name = item.name
    if item.price != None:
        inventory[item_id].price = item.price
    if item.brand != None:
        inventory[item_id].brand = item.brand
    return inventory[item_id]
@app.delete("/item/{item_id}")
def delete_item(item_id: int):
    if item_id not in inventory:
        raise HTTPException(404, detail= "Item ID does not exist.")
    del inventory[item_id]
    raise HTTPException(200, detail= "Item succesfully deleted.")
        
    
# /brandProducts Endpoint (GET)
@app.get("/brandProducts")
def get_item(brand: str = Query(None, description= "Get names and prices for all products of a particular brand")):
    output = []
    try:
        for item_id in inventory:
            if inventory[item_id].brand == brand:
                res_dict = {}
                product_name = inventory[item_id].name
                product_price = inventory[item_id].price
                res_dict[product_name] = product_price
                output.append(res_dict) 
        return output
    except:
        raise HTTPException(404, "No items found with that brand.")


