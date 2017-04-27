using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Text;
using System.Threading;
using RabbitMQ.Client;//RabbitMQ的客户端程序集
using RabbitMQ;

namespace GraduationProject
{
    public class RabbitMQHelper
    {
        public RabbitMQHelper()
        {
            Thread t1 = new Thread(new ThreadStart(Consumer));
            t1.IsBackground = false;
            t1.Start();
        }

        private void Consumer()
        {
            var factory = new ConnectionFactory();
            factory.HostName = "localhost";
            factory.UserName = "admin";
            factory.Password = "admin";

            using (var connection = factory.CreateConnection())
            {
                using (var channel = connection.CreateModel())
                {
                    channel.QueueDeclare("hello", false, false, false, null);

                    var consumer = new QueueingBasicConsumer(channel);
                    channel.BasicConsume("hello", true, consumer);

                    while (true)
                    {
                        //var ea = (BasicDeliverEventArgs)consumer.Queue.Dequeue();
                        var ea = consumer.Queue.Dequeue();
                        var body = ea.Body;
                        var message = Encoding.UTF8.GetString(body);

                        if (message == "1")
                        {
                            WorkflowHub hub = new WorkflowHub();
                            hub.Send("1");
                        }
                    }
                }
            }
        }
    }
}