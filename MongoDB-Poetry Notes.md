# Poetry

## 1. Installation

- Installer Script macOS

  - ```
    curl -sSL https://install.python-poetry.org | python3 -
    ```

- Use Vim / Nano to add Poetry bin directory is in your `PATH`

  - Open File

    ```
    nano ~/.zshrc
    ```

  - Add Path

    ```
    export PATH="$HOME/.local/bin:$PATH"
    ```

  - Apply Changes

    ```
    source ~/.zshrc
    ```

  - Check Installation

    ```
    poetry --version
    ```



## 2. Usage

### 2.1 Start a poetry project

```
poetry init
```

Guides you through creating a new `pyproject.toml` file for managing your project's dependencies and settings.



### 2.2 Configuring Virtual Environments

```
poetry config virtualenvs.in-project true
```

Sets the location for virtual environments to be within the project's directory. 

- Beneficial for managing environments on a per-project basis



### 2.3 Install

```
poetry install
```

Install all dependencies specified in `pyproject.toml`.



### 2.3 Running the Program

#### 2.3.1 Poetry Shell

```
poetry shell		# start shell
exit						# stop shell
```

- Opens a new shell with the virtual environment activated.
- Any command run after this will be within the context of the virtual environment.

#### 2.3.2 Poetry Run Command

```
poetry run python <FILE_NAME.py>
```

- Directly runs a specific command within the virtual environment without keeping the environment activated afterward.



### 2.4 Add Packages

```
poetry add <package_name>
```

- It can be useful to specify version constraints when adding a package

  - ```
    poetry add requests@^2.25
    ```



### 2.5 Remove Packages

```
poetry remove <package_name>
```

When removing a package (`poetry remove`), Poetry will also remove its dependencies, but only if they are not required by any other package in the project. If a dependency is needed by another package, it remains installed.



### 2.6 Extra Useful Commands

```
poetry update
```

Updates the packages to their latest versions within the constraints 

```
poetry lock
```

Regenerates the lock file (`poetry.lock`) for ensuring consistent installs across multiple environments or setups.

- `poetry.lock`: records exact versions of all dependencies used in a Poetry-managed Python project.
- `pyproject.toml`: is where dependencies are initially declared with possibly flexible version

```
poetry show
```

Lists installed packages and their dependencies for auditing / understanding project's dependency tree.

## 3. .toml vs .lock

**Purpose:**

- `pyproject.toml` is for declaring which dependencies you want to use.
- `poetry.lock` is for recording the exact versions of dependencies that were actually installed.

**Role in Dependency Management:**

- `pyproject.toml` helps in defining and managing the project dependencies at a high level.
- `poetry.lock` ensures consistency and repeatability by locking in specific versions.

Think of `pyproject.toml` as your shopping list for dependencies, where you specify what you need, and `poetry.lock` as the receipt that records what exactly was purchased and in what versions



# MongoDB

## 1. Get Started

1. Install Homebrew

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew --version
```

2. Install MongoDB Shell (mongosh)

```bash
brew install mongosh
mongosh --version
```

3. Connecting Option1: Connect to MongoDB (Terminal)

```bash
Database -> Connect -> Shell -> Copy Connection String to Terminal
mongosh "mongodb+srv://mangoapp01.x6pabsg.mongodb.net/" --apiVersion 1 --username yucpeng17
```

4. Connecting Option2: Connect to MongoDB (Python Code)

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



## 2. Creating Database

In MongoDB, a database is not actually created until it gets content.

MongoDB will create it automatically when first writes to the database

- Shell

```bash
db
- See which database you are using

show dbs
- See all available databases

use <dbName>
- Change or create a new database
```

- Python

```python
db = client['<DB Name>']
```



## 3. Creating Collections

In MongoDB, a collection is not actually created until it gets content.

Collection: Grouping of MongoDB Documents, like a Table in Relational DB

### 3.1 Explicit Way

```javascript
db.createCollection(<CollectionName>)
e.g. db.createCollection("people")
```

### 3.2 Implicit Way
```javascript
db.<CollectionName>.insertOne(<Object>)
e.g. db.people.insertOne({"name": "Eve"})
```

### 3.3 Python

```python
# MongoDB will create the collection when you first insert a document into it
collection = db['<COLLECTION NAME>']
```



## 4. Inserting Documents

Document: An object or like an entry of a Table in Relational DB

### 4.1 Insert a Single Document
```javascript
db.<Collectionname>.insertOne(<Object>)
<Object> => {...}
```

```
e.g.
db.people.insertOne({
    name: "Lily",
    gender: "female",
    height: "158cm",
    tags: ["student", "kind"],
    birth: Date()
})
```



### 4.2 Insert Multiple Documents

```javascript
db.<CollectionName>.insertMany(<ObjectLists>)
<ObjectLists> => [{...}, {...}]
```

```
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



## 5. Finding Data

- **`find()`:** 查询当前Collection下所有文档

```
e.g. db.COLLECTION.find()
```

- **`find(<filterObject>)`:** 查询所有满⾜参数对象`<filterObject>`中指定过滤条件的数据

```
查询Collection中所有等级是3的数据
e.g. db.COLLECTION.find({ level : 3})
```

- **`db.find(<filterObject>, <selectObject>)`:** 查询所有满⾜参数对象`<filterObject>`中指定过滤条件的数 据，并且只返回`<selectObject>`中指定的字段。英文：`Projection`
  - 1: Included / 0: Excluded
  - If Not specified : Excluded, unless `_id` is included by default

```
查询Collection中名字是关羽的数据，并且返回数据中只包含name和level字段
e.g. db.COLLECTION.find({name: "关羽"}, {name: 1, level: 1})
```

- **`findOne()`:**  与 find⽤法相同，找到满⾜过滤条件的对象，但是只返回第⼀条。

```
e.g. db.users.findOne({level: 1})
```

- **`countDocuments(<filterObject>)`:** 返回满⾜条件的记录的数量。

```
e.g. 
db.users.countDocuments()
db.users.countDocuments({ level: {$gt : 3}})
```

- **`limit()`:** 限制返回多少数据

```
db.people.find().limit(<NUMBER>)
```

- **`sort()`:** 使⽤给定的字段按照升序或者降序来排序。

```
// Example: Sorting in ascending order by age
db.users.find().sort({ age: 1 });

// Example: Sorting in descending order by name
db.users.find().sort({ name: -1 });
```

- **`skip()`:** 从头开始跳过给定数值的⽂档。

```
// Example: Skip the first 5 documents
db.users.find().skip(5);

// Example: Skip the first 10 documents and limit the results to 5 documents
db.users.find().skip(10).limit(5);
```





## 6. Updating Data

- **`updateOne()`:** 更新匹配过滤器的单个文档。

```
db.collection.updateOne(filter, update, options)
```

`filter`：用于查找文档的查询条件。
`update`：指定更新操作的文档或更新操作符。
`options`：可选参数对象，如 upsert、arrayFilters 等。

```
e.g.:
db.myCollection.updateOne(
    { name: "Alice" },                // 过滤条件
    { $set: { age: 26 } },            // 更新操作
    { upsert: false }                 // 可选参数
);
```

- **`updateMany()`:** 更新所有匹配过滤器的文档。

```javascript
db.collection.updateMany(filter, update, options)
```
`filter`：用于查找文档的查询条件。
`update`：指定更新操作的文档或更新操作符。
`options`：可选参数对象，如 upsert、arrayFilters 等。

```
e.g:
db.myCollection.updateMany(
    { age: { $lt: 30 } },             // 过滤条件
    { $set: { status: "active" } },   // 更新操作
    { upsert: false }                  // 可选参数
);
```

- **`replaceOne()`:** 替换匹配过滤器的单个文档，新的文档将完全替换旧的文档。

```
db.collection.replaceOne(filter, replacement, options)
```

`filter`：用于查找文档的查询条件。
`replacement`：新的文档，将替换旧的文档。
`options`：可选参数对象，如 upsert 等。

```
db.myCollection.replaceOne(
    { name: "Bob" },                  // 过滤条件
    { name: "Bob", age: 31 }          // 新文档
);
```

### 6.1 Operators in Upate

**`$set`**: Sets the value of a field in a document. If the field does not exist, it is created.

**`$unset, $inc, $mul`**

### 6.2 Insert if not found

Insert a new document if the specified filter does not match any existing documents

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



## 7. Delete Documents

We can delete documents by using the methods `deleteOne()` or `deleteMany()`.

These methods accept a query object. The matching documents will be deleted.

- **`deleteOne()`:** method will delete the first document that matches the query provided.

```
db.collection.deleteOne(filter, options)
```

`filter`：用于查找要删除的文档的查询条件。
`options`：一个可选参数对象。

```
db.people.deleteOne({ name: "Charlie" })
```

- **`deleteMany()`:** method will delete all documents that match the query provided.

```
db.collection.deleteMany(filter, options)
```

`filter`：用于查找要删除的文档的查询条件。
`options`：一个可选参数对象。

```
db.people.deleteMany({ gender: "male" })
```



## 8. Operators

### 8.1 Comparison

Compare field values to specified values.

- `$eq`: Values are equal
- `$ne`: Values are not equal
- `$gt`: Value is greater than another value
- `$gte`: Value is greater than or equal to another value
- `$lt`: Value is less than another value
- `$lte`: less than or equal to another value
- *`$in`: Value within an array
- *`$nin`: Value not within an array

```
- 如果不是比较的话：
db.collection.find({ age: 25 });

- 是比较的时候，就需要换成一个对象
e.g:
db.collection.find({ age: { $gt: 25 } });
db.collection.find({ age: { $in: [25, 30, 35] } });
db.collection.find({ age: { $gt: 25, $lt 50 } });

- $in
e.g.
db.collection.find({level: {$in: [3,4,5]}})
```

### 8.2 Logical

Combine multiple conditions.

- `$and`: Returns documents where both queries match

```
db.collection.find({ $and: [{ age: { $gt: 25 } }, { age: { $lt: 40 } }] });
```

- `$or`: Returns documents where either query matches

```
db.collection.fing({$or: [{level: { $gt: 4}}, {name: "GuanYu"}])
```

- `$nor`: Returns documents where both queries fail to match

```
db.collection.find({ $nor: [{ age: { $lt: 18 } }, { age: { $gt: 60 } }] });
```

- `$not`: Returns documents where the query does not match

```
db.collection.find({ age: { $not: { $gt: 25 } } });
```

### 8.3 Element

These operators are used to query fields based on their presence or type.

- **`$exists`**: Matches documents that have the specified field.

```
db.employees.find({ "emp_age": { $exists: true, $gte: 30}})
```

- **`$type`**: Matches documents where the field is of the specified BSON type.

```
db.employees.find({ "emp_age": { $type: "double"}})
```

### 8.4 Evaluation

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

- `$mod`

```
Example: Find documents where the remainder is 1000 when divided by 3000
db.inventory.find({"quantity": {$mod: [3000, 1000]}})
```



### 8.5 Fields

The following operators can be used to update fields:

- `$currentDate`: Sets the field value to the current date
- `$inc`: Increments the field value
- `$rename`: Renames the field
- `$set`: Sets the value of a field
- `$unset`: Removes the field from the document

### 8.5 Array

The following operators assist with updating arrays.

- `$addToSet`: Adds distinct elements to an array
- `$pop`: Removes the first or last element of an array
- `$pull`: Removes all elements from an array that match the query
- `$push`: Adds an element to an array



# 9. Aggregation

- Aggregation Pipelines Can Have One or More "Stages/Operations" to process and transform data
- The Order of These Stages Are Important because each stage processes the output of the previous stage

### 9.1 group

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



### 9.2 match

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



### 9.3 project

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



### 9.4 sort

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



### 9.5 limit

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



## 10. Index

- An index in MongoDB is a data structure that improves the speed of data retrieval operations



## 11. Validation

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



