

#ifndef NSTimer_PFSafeTimer_h
#define NSTimer_PFSafeTimer_h
#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN

@interface NSTimer (PFSafeTimer)

+ (NSTimer *)PF_ScheduledTimerWithTimeInterval:(NSTimeInterval)timeInterval block:
(void(^)(void))block repeats:(BOOL)repeats;

@end

NS_ASSUME_NONNULL_END



#endif /* NSTimer_PFSafeTimer_h */
