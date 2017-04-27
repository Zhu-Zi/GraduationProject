using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace GraduationProject.Controllers
{
    public class EditController : Controller
    {
        public ActionResult Index()
        {
            return View();
        }

        [ValidateInput(false)]
        public ActionResult Content(FormCollection fc)
        {
            var title = fc["title"];
            var content = fc["editor"];
            var area = fc["areaName"];

            MongoDBHelper.insterMongoDB(title, area, content);

            return Redirect("Index");
        }
    }
}