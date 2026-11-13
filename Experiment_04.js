use("lab_ex04");
db.student.drop();
db.posts.drop();

db.student.insertOne({
  regNo: "3014",
  name: "Test Student",
  course: { courseName: "MCA", duration: "3 Years" },
  address: { city: "Bangalore", state: "KA", country: "India" }
});

printjson(db.student.find().toArray());
printjson(db.student.find({ "regNo": "3014" }).toArray());

db.student.updateOne({ "regNo": "3014" }, { $set: { "name": "Viraj" } });
printjson(db.student.findOne({ "regNo": "3014" }));

db.student.deleteOne({ "regNo": "3014" });
print("students left: " + db.student.countDocuments({}));

const NEW_POST = {
  name: "Working with Arrays",
  user: "Database Rebel",
  desc: "Maintaining an array of objects in a document",
  content: "some content...",
  created: new Date(),
  updated: new Date(),
  tags: ["mongodb", "arrays"]
};
const postId = db.posts.insertOne(NEW_POST).insertedId;
printjson(db.posts.findOne());

const NEW_COMMENT = {
  user: "DB Learner",
  text: "Nice post, can I know more about the arrays in MongoDB?",
  updated: new Date()
};
db.posts.updateOne({ _id: postId }, { $push: { comments: NEW_COMMENT } });
db.posts.updateOne({ _id: postId },
  { $push: { comments: { user: "Database Rebel", text: "Thank you, please look for updates", updated: new Date() } } });
printjson(db.posts.findOne({ _id: postId }).comments);

const NEW_CONTENT = "Thank you, please look for updates - updated";
db.posts.updateOne(
  { _id: postId, "comments.user": "Database Rebel" },
  { $set: { "comments.$.text": NEW_CONTENT } }
);

db.posts.updateOne({ _id: postId }, { $pull: { comments: { user: "Database Rebel" } } });

db.posts.updateOne({ _id: postId }, { $set: { "comments.$[].likes": 0 } });

db.posts.updateOne({ _id: postId }, { $push: { comments: { user: "DB Learner", text: "Thanks for the updates!", updated: new Date() } } });
db.posts.updateOne(
  { _id: postId },
  { $inc: { "comments.$[ele].likes": 1 } },
  { arrayFilters: [ { "ele.user": "DB Learner", "ele.likes": { $exists: false } } ] }
);
printjson(db.posts.findOne({ _id: postId }).comments);
