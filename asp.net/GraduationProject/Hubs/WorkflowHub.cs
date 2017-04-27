using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using Microsoft.AspNet.SignalR;
using System.Threading.Tasks;

namespace GraduationProject
{
    public class WorkflowHub : Hub
    {
        public void Send(string message)
        {
            var context = GlobalHost.ConnectionManager.GetHubContext<WorkflowHub>();
            context.Clients.All.clientAddBroadcastMessage(message);
        }
    }
}