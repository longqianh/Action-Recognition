
/*用户界面
 可选择前置/后置摄像头
 最上方标签显示与RTMP服务器的连接情况
 点击下方键开始/停止检测
 */

#import "CustomPreview.h"
#import "LFLiveSession.h"
#import "UIView+YYAdd.h"
#import "ViewController.h"
#define SCREEN_WIDTH                      ([[UIScreen mainScreen]bounds].size.width)
#define SCREEN_HEIGHT                     ([[UIScreen mainScreen]bounds].size.height)

extern NSString *ID;
@interface CustomPreview() <LFLiveSessionDelegate>
@property (nonatomic, strong) UILabel       *stateLabel;

@property (nonatomic, strong) UIButton      *beautyButton;
@property (nonatomic, strong) UIButton      *cameraButton;
@property (nonatomic, strong) UIButton      *closeButton;
@property (nonatomic, strong) UIButton      *startLiveButton;
@property (nonatomic, strong) UIView        *backView;

@property (nonatomic, strong) LFLiveDebug   *debugInfo;
@property (nonatomic, strong) LFLiveSession *liveSession;
//@property (nonatomic, strong) NSString *tmp;
@end

@implementation CustomPreview

- (instancetype)initWithFrame:(CGRect)frame{
    if(self = [super initWithFrame:frame]){
        self.backgroundColor = [UIColor clearColor];
 
        [self checkVideoStatus];
        [self checkAudioStatus];
        
        [self setUI];
    }
    return self;
}

- (void)setUI
{
    [self addSubview:self.backView];
    [_backView addSubview:self.stateLabel];
    [_backView addSubview:self.resultLabel];
//    [_backView addSubview:self.closeButton];
    [_backView addSubview:self.cameraButton];
    [_backView addSubview:self.startLiveButton];
}

#pragma mark - Action

- (void)changeCapture:(id)sender
{
    AVCaptureDevicePosition devicePositon = _liveSession.captureDevicePosition;
    _liveSession.captureDevicePosition = (devicePositon == AVCaptureDevicePositionBack) ? AVCaptureDevicePositionFront : AVCaptureDevicePositionBack;
}


- (void)startLiveButton:(id)sender
{
    UIButton *startButton = (UIButton *)sender;
    startButton.selected = !startButton.selected;
    
    if(startButton.selected){
        [_startLiveButton setTitle:@"Stop Detection" forState:UIControlStateNormal];
        LFLiveStreamInfo *stream = [LFLiveStreamInfo new];
        NSString *addr=@"rtmp://124.70.69.88:1935/rtmplive/";
        addr = [addr stringByAppendingString:ID];
        stream.url = addr;
        
        [_liveSession startLive:stream];
    }else{
        [_startLiveButton setTitle:@"Start Detection" forState:UIControlStateNormal];
        [_liveSession stopLive];
    }
}

- (void)closeAction:(id)sender
{
    [_startLiveButton setTitle:@"Stop Detection" forState:UIControlStateNormal];
    [_liveSession stopLive];
}

#pragma mark - checkPrivateAuthority
- (void)checkVideoStatus
{
    __weak typeof(self) weakSelf = self;
    AVAuthorizationStatus status = [AVCaptureDevice authorizationStatusForMediaType:AVMediaTypeVideo];
    
    switch (status) {
        case AVAuthorizationStatusNotDetermined:{
            
            [AVCaptureDevice requestAccessForMediaType:AVMediaTypeVideo completionHandler:^(BOOL granted) {
                if (granted) {
                    dispatch_async(dispatch_get_main_queue(), ^{
                        [weakSelf.liveSession setRunning:YES];
                    });
                }
            }];
            break;
        }
            
        case AVAuthorizationStatusAuthorized:
            
            [weakSelf.liveSession setRunning:YES];
            break;
            
        case AVAuthorizationStatusDenied:
            break;
            
        case AVAuthorizationStatusRestricted:
            // 用户明确地拒绝授权，或者相机设备无法访问
            break;
            
        default:
            break;
    }
    
}


- (void)checkAudioStatus
{
    AVAuthorizationStatus status = [AVCaptureDevice authorizationStatusForMediaType:AVMediaTypeAudio];
    switch (status) {
        case AVAuthorizationStatusNotDetermined:{
            [AVCaptureDevice requestAccessForMediaType:AVMediaTypeAudio completionHandler:^(BOOL granted) {
            }];
            break;
        }
        case AVAuthorizationStatusAuthorized:{
            break;
        }
        case AVAuthorizationStatusDenied:
        case AVAuthorizationStatusRestricted:
            break;
        default:
            break;
    }
}


#pragma mark -- LFStreamingSessionDelegate
//显示当前流媒体服务器连接状态
- (void)liveSession:(nullable LFLiveSession *)session liveStateDidChange:(LFLiveState)state{
    NSLog(@"liveStateDidChange: %ld", state);
    switch (state) {
        case LFLiveReady:
            _stateLabel.text = @"Not Connected";
            break;
        case LFLivePending:
            _stateLabel.text = @"Connecting...";
            break;
        case LFLiveStart:
            _stateLabel.text = @"Connected";
            break;
        case LFLiveError:
            _stateLabel.text = @"Connection Error";
            break;
        case LFLiveStop:
            _stateLabel.text = @"Not Connected";
            break;
        default:
            break;
    }
}

//debug信息
- (void)liveSession:(nullable LFLiveSession *)session debugInfo:(nullable LFLiveDebug*)debugInfo{
    NSLog(@"debugInfo: %lf", debugInfo.dataFlow);
}

//错误信息
- (void)liveSession:(nullable LFLiveSession*)session errorCode:(LFLiveSocketErrorCode)errorCode{
    NSLog(@"errorCode: %ld", errorCode);
}

#pragma mark -- Getter Setter
- (LFLiveSession*)liveSession{
    if(!_liveSession){
        //   默认分辨率368 ＊ 640  音频：44.1 iphone6以上48  双声道  方向竖屏
        _liveSession = [[LFLiveSession alloc] initWithAudioConfiguration:[LFLiveAudioConfiguration defaultConfiguration] videoConfiguration:[LFLiveVideoConfiguration defaultConfigurationForQuality:LFLiveVideoQuality_Medium2]];
        
        _liveSession.delegate = self;
        _liveSession.preView = self;
    }
    return _liveSession;
}

- (UIView*)backView{
    if(!_backView){
        _backView = [UIView new];
        _backView.frame = self.bounds;
        _backView.backgroundColor = [UIColor clearColor];
        _backView.autoresizingMask = UIViewAutoresizingFlexibleWidth | UIViewAutoresizingFlexibleHeight;
    }
    return _backView;
}

- (UILabel*)stateLabel{
    if(!_stateLabel){
        _stateLabel = [[UILabel alloc] initWithFrame:CGRectMake(20, 20, 200, 40)];
        _stateLabel.text = @"Not Connected";
        _stateLabel.textColor = [UIColor whiteColor];
        _stateLabel.font = [UIFont boldSystemFontOfSize:14.f];
    }
    return _stateLabel;
}

- (UILabel*)resultLabel{
  
    if(!_resultLabel){
        _resultLabel = [[UILabel alloc] initWithFrame:CGRectMake(20, 20, 200, 40)];
        _resultLabel.top=20+_stateLabel.height;
        _resultLabel.text = @"Behavior: ";
        _resultLabel.textColor = [UIColor greenColor];
        _resultLabel.font = [UIFont boldSystemFontOfSize:18.f];
    }
    return _resultLabel;
}

- (UIButton*)closeButton{
    if(!_closeButton){
        _closeButton = [UIButton new];
        _closeButton.size = CGSizeMake(44, 44);
        _closeButton.left = self.width - 10 - _closeButton.width;
        _closeButton.top = 20;
        [_closeButton setImage:[UIImage imageNamed:@"close_preview"] forState:UIControlStateNormal];
        [_closeButton addTarget:self action:@selector(closeAction:) forControlEvents:UIControlEventTouchUpInside];

    }
    return _closeButton;
}

- (UIButton*)cameraButton{
    if(!_cameraButton){
        _cameraButton = [UIButton new];
        _cameraButton.size = CGSizeMake(44, 44);
        _cameraButton.origin = CGPointMake(_closeButton.left - 10 - _cameraButton.width, 20);
        _closeButton.top = 20;
        _cameraButton.left = self.width - 10 - _cameraButton.width;
        [_cameraButton setImage:[UIImage imageNamed:@"camra_preview"] forState:UIControlStateNormal];
        [_cameraButton addTarget:self action:@selector(changeCapture:) forControlEvents:UIControlEventTouchUpInside];

    }
    return _cameraButton;
}


- (UIButton*)startLiveButton{
    if(!_startLiveButton){
        _startLiveButton = [UIButton new];
        _startLiveButton.size = CGSizeMake(self.width - 60, 44);
        _startLiveButton.left = 30;
        _startLiveButton.bottom = self.height - 50;
        _startLiveButton.layer.cornerRadius = _startLiveButton.height/2;
        [_startLiveButton setTitleColor:[UIColor blackColor] forState:UIControlStateNormal];
        [_startLiveButton.titleLabel setFont:[UIFont systemFontOfSize:16]];
        [_startLiveButton setTitle:@"Start Detection" forState:UIControlStateNormal];
        [_startLiveButton setBackgroundColor:[UIColor colorWithRed:50 green:32 blue:245 alpha:1]];
        [_startLiveButton addTarget:self action:@selector(startLiveButton:) forControlEvents:UIControlEventTouchUpInside];

    }
    return _startLiveButton;
}

@end
