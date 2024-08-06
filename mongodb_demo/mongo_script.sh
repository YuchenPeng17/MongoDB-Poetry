# 1. Create Database
use MongoDB_Demo1

# 2. Create Collection
db.createCollection("Orders")

# 3. Insert/Create Document
db.Orders.insertOne({
    product: "toothbrush",
    quantity: 2,
    unit_price: 5.99,
    customer: "Mike",
})

db.Orders.insertMany([
  {
    product: "toothbrush",
    quantity: 2,
    unit_price: 5.99,
    customer: "Sarah",
  },
  {
    product: "shampoo",
    quantity: 1,
    unit_price: 7.99,
    customer: "John",
  },
  {
    product: "milk",
    quantity: 3,
    unit_price: 2.49,
    customer: "Mike",
  },
  {
    product: "eggs",
    quantity: 12,
    unit_price: 0.25, // Price per egg
    customer: "Sarah",
  },
  {
    product: "shampoo",
    quantity: 2,
    unit_price: 7.99,
    customer: "Mike",
  },
  {
    product: "toothbrush",
    quantity: 1,
    unit_price: 5.99,
    customer: "John",
  }
])

# 4. Find/Read Document
db.Orders.find()
    # Mike's Orders
db.Orders.find({customer: "Mike"})
    # Orders on shampoo
db.Orders.find({product: "shampoo"})
    # Mike's Orders using Projection
db.Orders.find({customer: "Mike"}, {product: 1, quantity: 1, _id: 0})
    # Number of Orders on Milk
db.Orders.countDocuments({ product: "milk" })
    # Who ordered the most?
db.Orders.find({}, {customer: 1, quantity: 1, _id: 0}).sort({quantity: -1})

# 5. Update Document
    # $set
    # Update the quantity of the first order for "toothbrush" from customer "Mike" to 3:
db.Orders.find({ product: "toothbrush", customer: "Mike" })
db.Orders.updateOne(
  { product: "toothbrush", customer: "Mike" },
  { $set: { quantity: 3 } }
);
    # Add a fiedl if unexisted
db.Orders.updateMany(
  {},
  { $set: { order_date: "2024-08-05" } }
);
    # $inc
    # Increase the unit_price of all "shampoo" products by 1:
db.Orders.find({ product: "shampoo"}, {_id: 0, product: 1, unit_price: 1, customer: 1})
db.Orders.updateMany({product:"shampoo"}, {$inc: {unit_price: 1}})

    # unset
    # Remove a Field from All Documents
db.Orders.updateMany(
  {},
  { $unset: { order_date: "" } }
);

    # $mul
    # Multiply the quantity of all "milk" products by 2:
db.Orders.find({product: "milk"})
db.Orders.updateMany(
  { product: "milk" },
  { $mul: { quantity: 2 } }
);
    # $upsert option
    # Insert a new document if the specified filter does not match any existing documents
db.Orders.updateOne(
  { product: "eggs", customer: "John" },
  { $set: { quantity: 10, unit_price: 0.25 } },
  { upsert: true }
);
db.Orders.updateOne(
  { product: "milk", customer: "Sarah" },
  { $set: { quantity: 2, unit_price: 2.49 } },
  { upsert: true }
);

# 6. Delete Document
    # Delete the first document where the product is "toothbrush" and the customer is "Mike":
db.Orders.deleteOne({ product: "toothbrush", customer: "Mike" });
    # Delete all documents where the product is "shampoo":
db.Orders.deleteMany({ product: "shampoo" });
    # Complex Conditions using Comparison & Logic Operators

# 7. Operators
    # Comparison Operators
db.Orders.find({ quantity: { $gt: 5 } })
db.Orders.find({ quantity: { $lte: 5 } })

    # Logical Operators
db.Orders.find({ $and: [{ quantity: { $gt: 5 } }, { customer: "Mike" }] })
db.Orders.find({ $or: [{ quantity: { $gt: 5 } }, { customer: "Mike" }] })
db.Orders.find({ $nor: [{ quantity: { $gt: 5 } }, { customer: "Mike" }] })

# 8. Aggregation
    # 1. Show how much did each customer spend in total and rank from high to low
db.Orders.aggregate(
    [
        {$match: {}},
        {$group: {
            _id: "$customer",
            total_spend: {$sum : {$multiply: ["$quantity", "$unit_price"]}}
        }},
        {$sort: {total_spend: -1}}
    ]
)

    # 2. Use aggregation to add a total_cost field for each document by 
    #    multipying quantity and unit_price
    db.Orders.updateMany(
        {},
        [
            {$set: {
                total_cost: {$multiply: ["$quantity", "$unit_price"]}
            }}
        ]
    )

