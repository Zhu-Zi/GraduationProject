using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using MongoDB.Driver;//MongoDB 驱动
using MongoDB.Bson;
using MongoDB.Driver.Builders;
using Newtonsoft.Json;

namespace GraduationProject
{
    public class IndexController : Controller
    {
        private static string connectionString = "mongodb://localhost:27017/graduationProject";
        private static string databaseName = "graduationProject";

        // GET: /Index/
        public ActionResult Index()
        {
            var mongoClient = new MongoClient(connectionString);

            MongoDatabase db = mongoClient.GetServer().GetDatabase(databaseName);
            //获取Studnet集合
            MongoCollection col = db.GetCollection("Absenteeism");

            //查询全部集合里的数据
            var result1 = col.FindAllAs<AbsenteeismModel>();

            List<AbsenteeismModel> absenteeismList = new List<AbsenteeismModel>();

            var flag = 1;
            foreach (var a in result1)
            {
                absenteeismList.Add(a);
                flag++;
                if (flag == 25)
                {
                    break;
                }
            }

            ViewData["AbsenteeismTableData"] = absenteeismList;

            var title = new List<string>();
            var content = new List<string>();

            for (int i = 0; i < 10; i++)
            {
                var titleData = "title" + (i + 1).ToString();
                title.Add(titleData);
                var contentData = "content" + (i + 1).ToString();
                content.Add(contentData);
            }

            ViewBag.title = title;
            ViewBag.content = content;

            var report = MongoDBHelper.selectMongoDB();

            if (report[0].Count() > 0 && report[1].Count() > 0)
            {
                ViewBag.title = report[0];
                ViewBag.content = report[1];
            }

            return View();
        }

        public JsonResult specialStuConsumptionAmount()
        {
            var mongoClient = new MongoClient(connectionString);

            MongoDatabase db = mongoClient.GetServer().GetDatabase(databaseName);
            //获取Studnet集合
            MongoCollection colAmount = db.GetCollection("specialStuConsumptionAmount");

            //查询全部集合里的数据
            var resultAmount = colAmount.FindAllAs<StuConsumptionAmountModel>();

            List<StuConsumptionAmountModel> amountList = new List<StuConsumptionAmountModel>();

            foreach (var item in resultAmount)
            {
                amountList.Add(item);
            }

            //Json.NET序列化
            string amountJsonData = JsonConvert.SerializeObject(amountList);

            return Json(amountJsonData);
        }

        public JsonResult specialStuConsumptionMachine()
        {
            var mongoClient = new MongoClient(connectionString);

            MongoDatabase db = mongoClient.GetServer().GetDatabase(databaseName);
            //获取Studnet集合
            MongoCollection colMachine = db.GetCollection("specialStuConsumptionMachine");

            //查询全部集合里的数据
            var resultMachie = colMachine.FindAllAs<StuConsumptionMachineModel>();

            List<StuConsumptionMachineModel> machineList = new List<StuConsumptionMachineModel>();

            foreach (var item in resultMachie)
            {
                machineList.Add(item);
            }

            //Json.NET序列化
            string machineJsonData = JsonConvert.SerializeObject(machineList);

            return Json(machineJsonData);
        }
    }
}