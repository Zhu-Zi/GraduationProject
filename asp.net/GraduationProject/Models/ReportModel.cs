using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using MongoDB.Driver;
using MongoDB.Bson;
using MongoDB.Driver.Builders;


namespace GraduationProject
{
    public class ReportModel
    {
        public ObjectId _id;//BsonType.ObjectId 这个对应了 MongoDB.Bson.ObjectId 
        public string title { get; set; }
        public string Area { get; set; }
        public string Content { get; set; }
        public string datetime { get; set; }
    }
}