using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using MongoDB.Driver;
using MongoDB.Bson;
using MongoDB.Driver.Builders;

namespace GraduationProject
{
    public class StuConsumptionAmountModel
    {
        public ObjectId _id;//BsonType.ObjectId 这个对应了 MongoDB.Bson.ObjectId 
        public string stuName { get; set; }
        public string amount { get; set; }
        public string times { get; set; }
    }
}