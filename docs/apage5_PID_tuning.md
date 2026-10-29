# PID tuning

Tuning the motor controller is crucial for maximizing the performance of any motor controller. Proper tuning ensures that the controller can swiftly respond to disturbances  like external forces or changes in the setpoint, without going unstable.

The process of tuning PID gains typically involves iterative adjustments, demanding a systematic approach to attain the desired performance level. Here's a fundamental guide for tuning the PID gains tailored for your Spectral controller:

*  Ensure that the motor's behavior won't lead to damage or injury in case of unexpected oscillations or erratic movements. 
* Secure the stator assembly firmly to prevent loosening in the event of oscillations.
* Conduct PID tuning without any gearbox or additional objects attached to the motor's rotor. This approach helps isolate the motor's response for more accurate tuning.
* If the default PID gains induce oscillations, reduce all gains until the system stabilizes. Incrementally adjust the gains, making small changes at a time.

To tune PID loops you can use UART protocol or CAN protocol. We recommend UART and here we will showcase example commands for UART protocol.
To tune the controller you will need to have it fully calibrated and without any active errors. Otherwise it will not allow you to enter any of the needed modes like: position, speed or current mode.

## Tuning cascade position, velocity and current controller

<img src="../assets/cascadeloop.png" alt="cascadeloop" width="1000"/> <br /> </p>

For tuning the cascaded structure, we should first focus on the inner loops and move outward.

### Tuning the Current controller

The innermost stage is always a current/torque controller that accepts torque/current requests and uses a PI controller to select voltage (PWM values) to achieve that current. You need to pick Kp and Ki for that loop. If they are too large, they can create audible noise or instability. If they are too small, the response to changes in commanded torque or disturbances will be reduced.

Torque bandwidth (current loop bandwidth) is measure of how fast a system can respond to those commands or disturbances. 
Current controller can be auto tuned during the calibration by selecting desired torque/current bandwidth (UART command #Cbw).  Motor calibration measures your motor’s  phase resistance and phase inductance. It uses this information and desired torque bandwidth setpoint to set its current controller gains.
The default current loop bandwidth is 500 Hz (`#Cbw`). 

**Generally in industry bandwidths of more than 800 Hz are standard.** Higher torque bandwidth is desired for legged robots, or other applications where it is necessary to respond to external disturbances as fast as possible. Higher torque bandwidths will result in audible noise and if they are too large in drive instability.

We recommend tuning the current controller gains with auto tune feature in #Cal command.

If you want to tune it by hand:

1. Increase proportional gain until system starts to become unstable (it will oscillate or create humming sounds). Use command #Kpiq
2. Reduce that value by 20% and confirm that there is no oscillation. If it still oscillates reduce it more.
3. Now slowly increase Ki until system starts to become unstable (it will oscillate or create humming sounds). Use command #Kiiq
4. Reduce the value slightly until it becomes stable.

To test the current controller you will need to issue a #Iq VALUE Command. VALUE will be the value of Iq current you want as a setpoint, make sure it is not too large and that your motor can handle it.

### Tuning the velocity controller

So after making sure the Torque loop works in an acceptable manner, we can start tuning velocity controller. 

1. Controllers come preloaded with weak gains. If it oscillates with them reduce Kp and Ki to 0.
2. Increase proportional velocity gain until system starts to become unstable (it will oscillate or create humming sounds). Use command #Kpv
3. Reduce that value by 20% and confirm that there is no oscillation. If it still oscillates reduce it more.
4. Now slowly increase Ki until system starts to become unstable (it will oscillate or create humming sounds). Use command #Kiv

!!! tip "Tip"
    Bear in mind that the Ki gain is highly sensitive as it acts as an integrator accumulating over time. Setting excessively high values for Ki can potentially render your system unstable. For some motors, setting the Speed controller Ki to zero and relying solely on the Speed controller Kp gain might be adequate. However, in such cases, getting a zero steady-state error is hard. Therefore, the Ki gain plays a important role in both reaching the desired goal and sustaining it over time.

5. Reduce the value of Ki slightly until it becomes stable.
6. If you think you tuned your controller start to experiment with different speeds and see how it reacts and tracks them.

 Give the motor #V VALUE command. VALUE will be the value of velocity in encoder ticks/s we want to achieve, make sure it is not to large or too small and that your motor can handle it.

### Tuning the position controller

1. Controllers come preloaded with weak proportional gain. If it oscillates with it reduce it to 0.
2. Start increasing the proportional gain. The system will use the already-tuned current and velocity controller as inner loops. Use command #Kpp
3. Increase until you notice overshoot in the position response. If overshooting is excessive or oscillations start, reduce the gain slightly until satisfactory performance is achieved without instability.
4. Ideally, the response should be quick to reach the desired position but without excessive oscillations.

You can set motor position command by using #P VALUE. VALUE will be the value of position in encoder ticks.

### Testing the cascade controller

If you think you system is tuned:

1. Conduct tests across the entire spectrum of operational conditions to verify stability and performance under various scenarios.
2. If possible, introduce disturbances such as changes in load to assess the system's robustness and response to external factors.
3. Based on real-world performance observations, adjust the gains as necessary to optimize the system's behavior and ensure consistent performance across different conditions.
4. If you think you tuned your controller start to experiment with different speeds and see how it reacts and tracks them.

## Tuning impedance PD controller

<img src="../assets/PDloop.png" alt="PDloop" width="1000"/> <br /> </p>

## Velocity limits

To get an estimate of how fast your motor can spin use this formula:<br />
Max_velocity [encoder ticks /s] = ((0.8 * Vbus * KV) * 16384) / 60 

## Current limits

Changes from motor to motor. 
The MOSFET driver stage shuts down by itself on overcurrent or overtemperature, which the driver reports as a driver error. The firmware clamps the current limit `#Ilim` to 2800 mA; this release does not raise a current error of its own.
Motor temperature is important here. To not to destroy your motor; carefully select your current limits based on rated power of the motor your testing.

You hear crunching and whining sounds. Your current limit might be too high, lower it.

## Integral accumulator reset

Here's why resetting the integral accumulator might be advantageous:

* Segmented Velocity Profile: If your velocity profile consists of distinct segments with different velocities, resetting the integral accumulator when transitioning between segments can help prevent integral windup. This ensures that the integral term doesn't accumulate excessive error during the transition, which could lead to overshoot or instability.

* Reducing Error Accumulation: Resetting the integral term allows the controller to start accumulating error from the new setpoint, which can help maintain accuracy and responsiveness, particularly if there are sudden changes or disturbances in the system.

* Improved Response: By resetting the integral term, you ensure that the controller responds promptly to changes in the velocity profile without being influenced by past errors that may no longer be relevant.

However, it's essential to consider the dynamics of your system and the characteristics of the velocity profile. If the transitions between velocity segments are smooth and gradual, or if the feedforward component adequately compensates for changes in velocity, resetting the integral term may not be necessary.

Ultimately, it may require some experimentation and tuning to determine the optimal behavior for your specific application, taking into account factors such as stability, response time, and accuracy.