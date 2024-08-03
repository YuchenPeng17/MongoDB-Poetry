# Get Started

Install Homebrew

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew --version
```

Install MongoDB Shell (mongosh)

```bash
brew install mongosh
mongosh --version
```

Option1: Connect to MongoDB (Terminal)

```bash
Database -> Connect -> Shell -> Copy Connection String to Terminal
mongosh "mongodb+srv://mangoapp01.x6pabsg.mongodb.net/" --apiVersion 1 --username yucpeng17
```

Option2: Connect to MongoDB (Python Code)

```python
# 1. Load the configuration file
def load_config():
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)
config = load_config()
password = config['mongo']['password']

# 2. Connect to MongoDB
uri = f"mongodb+srv://yucpeng17:{password}@mangoapp01.x6pabsg.mongodb.net/?retryWrites=true&w=majority&appName=MangoApp01"
client = MongoClient(uri)
```

- `Connection String`: Includes the necessary details for connecting to a MongoDB server



# Creating a Database

- In MongoDB, a database is not actually created until it gets content.
```bash
db
- See which database you are using

show dbs
- See all available databases

use <dbName>
- Change or create a new database
```

- Python
  - If `DB Name` does not exist, MongoDB will create it automatically when you first perform an operation that writes to the database
  - Such as inserting a document into a collection within that database.

```python
db = client['<DB Name>']
```



# Creating Collections 

- In MongoDB, a collection is not actually created until it gets content.
- Collection: Grouping of MongoDB Documents, like a Table in Relational DB

## Explicit Way

```javascript
db.createCollection(<CollectionName>)
e.g db.createCollection("people")
```

## Implicit Way
```javascript
db.<CollectionName>.insertOne(<Object>)
db.people.insertOne({"name": "Eve"})
```

- Python

```python
# MongoDB will create the collection when you first insert a document into it
collection = db['<COLLECTION NAME>']
```



# ##################



# Inserting Documents

- Document: An object or like an entry of a Table in Relational DB

## Insert a Single Document
```javascript
db.<Collectionname>.insertOne(<Object>)

e.g:
db.people.insertOne({
    name: "Lily",
    gender: "female",
    height: "158cm",
    tags: ["student", "kind"],
    birth: Date()
})
```

## Insert Multiple Documents
```javascript
db.<CollectionName>.insertMany(<ObjectLists>)

e.g:
db.people.insertMany([
    {
        name: "Alice",
        gender: "female",
        height: "165cm",
        tags: ["developer", "friendly"],
        birth: new Date("1992-06-15")
    },
    {
        name: "Bob",
        gender: "male",
        height: "175cm",
        tags: ["teacher", "patient"],
        birth: new Date("1985-02-20")
    },
    {
        name: "Charlie",
        gender: "non-binary",
        height: "170cm",
        tags: ["designer", "creative"],
        birth: new Date("1990-11-05")
    }
]);
```



# Finding Data

## Find Multiple Documents
```javascript
db.people.find(<{...}>)
```
- This method accepts a query object. If left empty, all documents will be returned.

## Find One Document
```javascript
db.people.findOne(<{...}>)
```
- This method accepts a query object. If left empty, it will return the first document it finds.

## Querying Data
- To query or filter data, include a query in the `find()` or `findOne()` methods.
```javascript
db.people.find({gender: "female"})
```

## Projection
- A second parameter for both `find` methods.
- This parameter is an object that describes which fields/keys to include in the results.
  - `field/key: 1` indicates that the field should be included in the result.
  - `field/key: 0` indicates that the field should be excluded from the result.
  - Fields not specified in the projection are treated as excluded by default.
```javascript
db.people.find({}, { name: 1, gender: 1, _id: 0 });
```



# Updating Data

- `query`: 1st Partameter, Object to define which documents should be updated.
- `update`: 2nd Parameter, Object defining the updated data.
- `$set:`

## Update One Document

```javascript
db.people.updateOne(query, $set: update)
```
## Update Multiple Documents
```javascript
db.people.updateMany(query, $set: update)
```
```
e.g:
db.people.updateOne({name:"Bob"}, {$set: {height: "180cm"}})
```

## Insert if not found

If you would like to insert the document if it is not found, you can use the `upsert` option.

```
db.people.updateOne( 
  { name: "Eve" }, 
  {
    $set: 
      {
        gender: "female",
        height: "170cm",
        tags: ["fighter", "game character"]
      }
  }, 
  { upsert: true }
)
```

# Delete Documents

We can delete documents by using the methods `deleteOne()` or `deleteMany()`.

These methods accept a query object. The matching documents will be deleted.

## Delete One Document

 `deleteOne()`: method will delete the first document that matches the query provided.

```
db.people.deleteOne({ name: "Charlie" })
```

## Delete Many Documents

`deleteMany()`: method will delete all documents that match the query provided.

```
db.people.deleteMany({ gender: "male" })
```



# ##################



# Query Operators

## Comparison

The following operators can be used in queries to compare values:

- `$eq`: Values are equal
- `$ne`: Values are not equal
- `$gt`: Value is greater than another value
- `$gte`: Value is greater than or equal to another value
- `$lt`: Value is less than another value
- `$lte`: Value is less than or equal to another value
- `$in`: Value is matched within an array

```
e.g:
db.collection.find({ age: { $gt: 25 } });
db.collection.find({ age: { $in: [25, 30, 35] } });
```

## Logical

The following operators can logically compare multiple queries. 

- `$and`: Returns documents where both queries match

```
db.collection.find({ $and: [{ age: { $gt: 25 } }, { age: { $lt: 40 } }] });
```

- `$or`: Returns documents where either query matches
- `$nor`: Returns documents where both queries fail to match

```
db.collection.find({ $nor: [{ age: { $lt: 18 } }, { age: { $gt: 60 } }] });
```

- `$not`: Returns documents where the query does not match

```
db.collection.find({ age: { $not: { $gt: 25 } } });
```

## Evaluation

The following operators assist in evaluating documents.

- `$regex`: Allows the use of regular expressions when evaluating field values
  - ` regular expressions`: sequences of characters that form search patterns. !!Go Searching If Using!!

```
Example: Find documents where the `name` field starts with the letter 'A'.
db.collection.find({ name: { $regex: '^A' } });
```

- `$text`: Performs a text search
- `$where`: Uses a JavaScript expression to match documents

```
db.collection.find({ $where: function() {
    return this.age > 25 && this.name.startsWith('J');
} });
```

## Fields

The following operators can be used to update fields:

- `$currentDate`: Sets the field value to the current date
- `$inc`: Increments the field value
- `$rename`: Renames the field
- `$set`: Sets the value of a field
- `$unset`: Removes the field from the document

## Array

The following operators assist with updating arrays.

- `$addToSet`: Adds distinct elements to an array
- `$pop`: Removes the first or last element of an array
- `$pull`: Removes all elements from an array that match the query
- `$push`: Adds an element to an array



# ##################



# Aggregation

- Aggregation Pipelines Can Have One or More "Stages/Operations" to process and transform data
- The Order of These Stages Are Important because each stage processes the output of the previous stage
- 





## group

- The `$group` stage in MongoDB Aggregation is used to group documents by a specified key AND THEN to perform aggregations on the grouped data.
- You can use various accumulator expressions like `$sum`, `$avg`, `$min`, `$max`, and `$push` within the `$group` stage to calculate aggregated values.

```
Suppose we have a collection of sales data with the following documents:
[
  { "product": "A", "price": 10, "quantity": 2 },
  { "product": "B", "price": 20, "quantity": 1 },
  { "product": "A", "price": 10, "quantity": 1 },
  { "product": "B", "price": 20, "quantity": 2 },
  { "product": "A", "price": 10, "quantity": 3 }
]

We want to group these documents by the product field and calculate the total quantity sold for each product.
Aggregation Pipeline:
[
  {
    "$group": {
      "_id": "$product",
      "totalQuantity": { "$sum": "$quantity" }
    }
  }
]

Result:
[
  { "_id": "A", "totalQuantity": 6 },
  { "_id": "B", "totalQuantity": 3 }
]
```

`"_id": "$product"`: Groups the documents by the `product` field.

`"totalQuantity": { "$sum": "$quantity" }`: Calculates the total quantity for each group by summing the `quantity` field.

**_id** (Mandatory)

- The `_id` field is required in the `$group` stage and is used to specify the grouping key. Each unique value of this key will be a separate group in the output.
- The value of `_id` can be any valid MongoDB expression. If you want a single group for all documents, you can set `_id` to `null`.

**Accumulators** (Optional)

- These are fields where you specify the aggregation operation to be performed on each group.



**What!? There are two `_id`!!?**

- **_id in $group**: In the `$group` stage, the `_id` field is used to <u>specify the key by which to group documents</u>.
  - Grouping Key: It defines how documents are grouped together and <u>what value is used as the key for each group</u>.

- **Document _id**: The `_id`field that MongoDB assigns to each document by default (the ObjectId).
  - The original `_id` field (e.g., `ObjectId("60c72b2f9af1c88b8e620b7a")`) is <u>a unique identifier for each document, automatically generated by MongoDB.</u>



## match

The `$match` stage in MongoDB aggregation is used to filter documents that pass through the pipeline based on specified conditions. It operates similarly to the `WHERE` clause in SQL, allowing you to include only those documents that meet certain criteria.

- **Efficiency**: Placing `$match` early in the pipeline can improve performance by reducing the number of documents processed in subsequent stages.

```
1. Suppose we have a collection of documents representing orders:
[
  { "orderId": 1, "product": "A", "quantity": 5, "status": "shipped" },
  { "orderId": 2, "product": "B", "quantity": 10, "status": "pending" },
  { "orderId": 3, "product": "A", "quantity": 3, "status": "shipped" },
  { "orderId": 4, "product": "C", "quantity": 8, "status": "cancelled" },
  { "orderId": 5, "product": "B", "quantity": 7, "status": "shipped" }
]

2. We want to filter these documents to include only those with the status "shipped":
Aggregation Pipeline:
[
	{
		"$match": { "status": "shipped" }
	}
]

3. Results:
[
  { "orderId": 1, "product": "A", "quantity": 5, "status": "shipped" },
  { "orderId": 3, "product": "A", "quantity": 3, "status": "shipped" },
  { "orderId": 5, "product": "B", "quantity": 7, "status": "shipped" }
]
```

**Why bother have a `$match` rather than stick to `find`?**

1. Pipelines&Queries
   1. **Aggregation Pipelines**: `$match` is used as part of a multi-stage pipeline that can perform complex data transformations and aggregations.
   2. **find()**: Primarily used for straightforward queries to retrieve documents without additional processing.



## project

The `$project` stage in MongoDB aggregation is used to reshape documents by including, excluding, or adding fields. It allows you to control which fields are passed along to the next stage of the pipeline.

- **Field Inclusion/Exclusion**: Specify which fields to include or exclude in the output documents.
- **Computed Fields**: Create new fields or transform existing fields using expressions.
- **Default Behavior**: If a field is not specified, it will be excluded from the output. If `_id`  is not explicitly excluded (set to 0), it will be included by default.

```
1. Suppose we have a collection of documents representing sales:
[
  { "product": "A", "price": 10, "quantity": 2, "category": "electronics" },
  { "product": "B", "price": 20, "quantity": 1, "category": "household" },
  { "product": "A", "price": 10, "quantity": 1, "category": "electronics" }
]

2. We want to create a new field called totalValue that multiplies price by quantity and include only the product and totalValue fields in the output.
[
  {
    "$project": {
      "product": 1,
      "totalValue": { "$multiply": ["$price", "$quantity"] },
      "_id": 0
    }
  }
]

3. Results:
[
  { "product": "A", "totalValue": 20 },
  { "product": "B", "totalValue": 20 },
  { "product": "A", "totalValue": 10 }
]
```



## sort

The `$sort` stage in MongoDB aggregation is used to sort the documents in the pipeline based on specified fields

- **Syntax**: The `$sort` stage takes an object where the keys are the field names and the values are the sort order.

  - `1` for ascending order.

  - `-1` for descending order.

- MongoDB supports sorting on various data types including strings, dates, booleans...

```
1. Suppose we have a collection of documents representing products:
[
  { "product": "A", "price": 10, "quantity": 2 },
  { "product": "B", "price": 20, "quantity": 1 },
  { "product": "C", "price": 15, "quantity": 5 }
]

2. We want to sort these documents by `price` in descending order.
Aggregation Pipeline:
[
  {
    "$sort": { "price": -1 }
  }
]

3. Results:
[
  { "product": "B", "price": 20, "quantity": 1 },
  { "product": "C", "price": 15, "quantity": 5 },
  { "product": "A", "price": 10, "quantity": 2 }
]
```



## limit

The `$limit` stage in MongoDB aggregation is used to limit the number of documents passed to the next stage in the pipeline. This is particularly useful for returning a subset of results, such as the top N documents based on some criteria.

- **Syntax**: The `$limit` stage takes a single numeric argument that specifies the maximum number of documents to pass along.
- **Use Case**: Often used in conjunction with `$sort` to return the top results, such as top 5 highest scores, most recent entries, etc.

```
1. Suppose we have a collection of documents representing students with their scores:
[
  { "name": "Alice", "score": 95 },
  { "name": "Bob", "score": 90 },
  { "name": "Charlie", "score": 85 },
  { "name": "David", "score": 80 },
  { "name": "Eva", "score": 75 }
]

2. We want to retrieve the top 3 students based on their scores.
[
  { "$sort": { "score": -1 } },  // Sort by score in descending order
  { "$limit": 3 }                // Limit the result to top 3 students
]

3. Results:
[
  { "name": "Alice", "score": 95 },
  { "name": "Bob", "score": 90 },
  { "name": "Charlie", "score": 85 }
]
```



# ##################



# Index

- An index in MongoDB is a data structure that improves the speed of data retrieval operations









# Validation

- In MongoDB, a schema defines the structure and organization of data in a collection.
- Unlike traditional SQL databases, MongoDB is schema-less, meaning it does not enforce a fixed schema at the database level.
- However, schemas can be enforced at the application level using tools like Mongoose (for Node.js), which allow developers to define and enforce a schema for MongoDB collections.

```json
db.createCollection("posts", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [ "title", "body" ],
      properties: {
        title: {
          bsonType: "string",
          description: "Title of post - Required."
        },
        body: {
          bsonType: "string",
          description: "Body of post - Required."
        },
        category: {
          bsonType: "string",
          description: "Category of post - Optional."
        },
        likes: {
          bsonType: "int",
          description: "Post like count. Must be an integer - Optional."
        },
        tags: {
          bsonType: ["string"],
          description: "Must be an array of strings - Optional."
        },
        date: {
          bsonType: "date",
          description: "Must be a date - Optional."
        }
      }
    }
  }
})
```



