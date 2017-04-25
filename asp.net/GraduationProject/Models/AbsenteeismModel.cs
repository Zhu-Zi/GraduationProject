using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using MongoDB.Driver;
using MongoDB.Bson;
using MongoDB.Driver.Builders;

namespace GraduationProject
{
    public class AbsenteeismModel
    {
        public ObjectId _id;//BsonType.ObjectId 这个对应了 MongoDB.Bson.ObjectId 
        public string collageName { get; set; }
        public string className { get; set; }
        public string studentName { get; set; }
        public string datetime { get; set; }
        public string week { get; set; }
        public int classNum { get; set; }
        public string studentConsumptions { get; set; }
        public string classContent { get; set; }
    }
}