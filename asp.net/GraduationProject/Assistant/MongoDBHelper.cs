using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using MongoDB.Driver;//MongoDB 驱动
using MongoDB.Bson;
using MongoDB.Driver.Builders;

namespace GraduationProject
{
    public static class MongoDBHelper
    {
        private static string connectionString = "mongodb://localhost:27017/graduationProject";
        private static string databaseName = "graduationProject";
        
        public static void insterMongoDB(string title,string area, string content)
        {
            var mongoClient = new MongoClient(connectionString);
            MongoDatabase db = mongoClient.GetServer().GetDatabase(databaseName);

            ReportModel report = new ReportModel();

            report.title = title;
            report.Area = area;
            report.Content = content;
            report.datetime = DateTime.Now.ToString();

            MongoCollection col = db.GetCollection("Report");
            col.Insert<ReportModel>(report);
        }

        public static IList<List<string>> selectMongoDB()
        {
            List<List<string>> resultList = new List<List<string>>();
            List<string> titel = new List<string>();
            List<string> content = new List<string>();

            var mongoClient = new MongoClient(connectionString);
            MongoDatabase db = mongoClient.GetServer().GetDatabase(databaseName);
            //获取Studnet集合
            MongoCollection col = db.GetCollection("Report");
            //查询全部集合里的数据
            var resultData = col.FindAllAs<ReportModel>();

            List<string> area = new List<string>();

            foreach (var item in resultData)
            {
                if (area.All(x => x != item.Area)) 
                {
                    area.Add(item.Area);
                } 
            }

            foreach (var item in area)
            {
                var dataList = resultData.Where(x => x.Area == item).ToList();
                var aimData = dataList.Last();

                titel.Add(aimData.title);
                content.Add(aimData.Content);
            }

            resultList.Add(titel);
            resultList.Add(content);

            return resultList;
        }
    }
}