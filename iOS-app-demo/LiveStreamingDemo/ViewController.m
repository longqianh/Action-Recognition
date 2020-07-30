
/*控制文件说明
 控制界面显示
 向服务端请求随机的用户识别ID号
 将直播流推送到rtmp服务器，每段ts视频为3秒，命名为之前获取的ID号
 每1.5s发送GET请求更新当前结果
 */

#import "ViewController.h"
#import "CustomPreview.h"
#import "NSTimer+PFSafeTimer.h"
#import <sys/socket.h>
#import <netinet/in.h>
#import <arpa/inet.h>

NSString * ID;//用户识别ID
CustomPreview *customPreview;
@interface ViewController ()<NSURLSessionDataDelegate>
@property (nonatomic, strong) NSTimer       *timer;//定时器
@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    customPreview = [[CustomPreview alloc] initWithFrame:self.view.bounds];
    //从服务器获取ID号
    [self GetRoom];
    
    //定时发出GET请求获取当前行为
    __weak typeof(self) weakSelf = self;
    
    self.timer = [NSTimer PF_ScheduledTimerWithTimeInterval:1.5 block:^{
        __strong typeof(self) strongSelf = weakSelf;        
       [strongSelf Request];
       //NSLog(CurBehavior);
    } repeats:YES];
   
    //加载用户界面
    [self.view addSubview:customPreview];
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
}

- (UIInterfaceOrientationMask)supportedInterfaceOrientations
{
    return UIInterfaceOrientationMaskPortrait;
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)toInterfaceOrientation
{
    return YES;
}

//获取ID
-(void)GetRoom{
    NSLog(@"GetRoom");
    //网络请求
    NSURL *url = [NSURL URLWithString:@"http://124.70.69.88:443/getroom"];
    NSURLRequest *request = [NSURLRequest requestWithURL:url];
    NSURLSession *session = [NSURLSession sharedSession];
    NSURLSessionDataTask *dataTask = [session dataTaskWithRequest:request completionHandler:^(NSData * _Nullable data, NSURLResponse * _Nullable response, NSError * _Nullable error) {
        if (error == nil&&data != nil)
        {
           ID  =[[NSString alloc] initWithData:data encoding:NSUTF8StringEncoding];
            NSLog(@"%@",ID);
        }
    }];
    [dataTask resume];
}

//获取当前检测结果，结果显示到用户界面
-(void)Request
{
    NSLog(@"GetRequest");
    NSString *query=@"http://124.70.69.88:443/getresult?ID=";
    query = [query stringByAppendingString:ID];
    NSURL *url = [NSURL URLWithString:query];
    NSURLRequest *request = [NSURLRequest requestWithURL:url];
    NSURLSession *session = [NSURLSession sharedSession];
    NSString * __block res=@"Behavior: None";
    NSURLSessionDataTask *dataTask = [session dataTaskWithRequest:request completionHandler:^(NSData * _Nullable data, NSURLResponse * _Nullable response, NSError * _Nullable error) {
        if (error == nil&&data != nil)
        {
            NSString *temp=[[NSString alloc] initWithData:data encoding:NSUTF8StringEncoding];
            NSString *result=@"Behavior: ";
            result = [result stringByAppendingString:temp];
            dispatch_async(dispatch_get_main_queue(),^{
                customPreview.resultLabel.text=result;
                
            });
        }
        else{
            dispatch_async(dispatch_get_main_queue(),^{
                customPreview.resultLabel.text=res;
            });
        }
    }];
    [dataTask resume];
}


- (void)dealloc {
    
    //    [self.timer stopTimer];
    NSLog(@"%s",__func__);
}


@end
