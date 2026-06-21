data = read.csv("~/BioM2Lab/Branch_label/combined_node_branch.csv", header=T)

### 1) OVERALL
## D1 vs NODE AREA
#plot
plot(data$D1_radius, data$RADIUS_AREA_CM, main="Overall D1 vs NODE_RADIUS_AREA", 
     xlab="D1 (radius, cm)", ylab="NODE_RADIUS_AREA (cm)")
line = lm(RADIUS_AREA_CM~D1_radius, data=data)
abline(line, col="red", lwd=2)
#residuals
residuals = residuals(line)
mse = mean(residuals^2) # mse = 1.421077
mae = mean(abs(residuals)) # mae = 0.9169009
#summary
summary(line)
#confidence interval
confint(line)
#r^2
summary(line)$r.squared # r^2 = 0.3516414
summary(line)$adj.r.squared # 0.3494056

## D1 vs NODE CIRCUMFERENCE
#plot
plot(data$D1_radius, data$RADIUS_CIRC_CM, main="Overall D1 vs 
     NODE_RADIUS_CIRCUMFERENCE", xlab="D1 (radius, cm)", 
     ylab="NODE_RADIUS_CIRCUMFERENCE (cm)")
line2 = lm(RADIUS_CIRC_CM~D1_radius, data=data)
abline(line2, col="red",lwd=2)
#residuals
residuals2 = residuals(line2)
mse2 = mean(residuals2^2) # mse = 0.01289076
mae2 = mean(abs(residuals2)) # mae = 0.08439664
#summary
summary(line2)
#confidence interval
confint(line2)
#r^2
summary(line2)$r.squared # r^2 = 0.3567422
summary(line2)$adj.r.squared # 0.354524



### 2) SECTIONS
## Section 1: D1 <= 5
s1 = subset(data, D1_radius <= 5)
# AREA
plot(s1$D1_radius, s1$RADIUS_AREA_CM, main="Section 1 (D1 <=5): 
     D1 vs NODE_RADIUS_AREA", xlab="D1 (radius, cm)", 
     ylab="NODE_RADIUS_AREA (cm)")
line3 = lm(RADIUS_AREA_CM~D1_radius, data=s1)
abline(line3, col="red", lwd=2)
#residuals
residuals3 = residuals(line3)
mse3 = mean(residuals3^2) # mse = 1.375091
mae3 = mean(abs(residuals3)) # mae = 0.9031168
#summary
summary(line3)
#confidence interval
confint(line3)
#r^2
summary(line3)$r.squared # r^2 = 0.06662212
summary(line3)$adj.r.squared # 0.06241772

# CIRCUMFERENCE
plot(s1$D1_radius, s1$RADIUS_CIRC_CM, main="Section 1 (D1 <=5): 
     D1 vs NODE_RADIUS_CIRCUMFERENCE", xlab="D1 (radius, cm)", 
     ylab="NODE_RADIUS_CIRCUMFERENCE (cm)")
line4 = lm(RADIUS_CIRC_CM~D1_radius, data=s1)
abline(line2, col="red",lwd=2)
#residuals
residuals4 = residuals(line4)
mse4 = mean(residuals4^2) # mse = 0.01051897
mae4 = mean(abs(residuals4)) # mae = 0.07591718
#summary
summary(line4)
#confidence interval
confint(line4)
#r^2
summary(line4)$r.squared # r^2 = 0.0571738
summary(line4)$adj.r.squared # 0.05292683


## Section 2: 5 <= D1 < 10
s2 = subset(data, 5 < D1_radius & D1_radius <= 10)
# AREA
plot(s2$D1_radius, s2$RADIUS_AREA_CM, main="Section 2 (5 < D1 <= 10): D1 vs NODE_RADIUS_AREA", xlab="D1 (radius, cm)", ylab="NODE_RADIUS_AREA (cm)")
line5 = lm(RADIUS_AREA_CM~D1_radius, data=s2)
abline(line5, col="red", lwd=2)
#residuals
residuals5 = residuals(line5)
mse5 = mean(residuals5^2) # mse = 1.269907
mae5 = mean(abs(residuals5)) # mae = 0.8826381
#summary
summary(line5)
#confidence interval
confint(line5)
#r^2
summary(line5)$r.squared # r^2 = 0.01308869
summary(line5)$adj.r.squared # -0.009862732

# CIRCUMFERENCE
plot(s2$D1_radius, s2$RADIUS_CIRC_CM, main="Section 2 (5 < D1 <= 10): 
     D1 vs NODE_RADIUS_CIRCUMFERENCE", xlab="D1 (radius, cm)", 
     ylab="NODE_RADIUS_CIRCUMFERENCE (cm)")
line6 = lm(RADIUS_CIRC_CM~D1_radius, data=s2)
abline(line6, col="red",lwd=2)
#residuals
residuals6 = residuals(line6)
mse6 = mean(residuals6^2) # mse = 0.01646555
mae6 = mean(abs(residuals6)) # mae = 0.1059104
#summary
summary(line6)
#confidence interval
confint(line6)
#r^2
summary(line6)$r.squared # r^2 = 0.01147834
summary(line6)$adj.r.squared # -0.01151054


## Section 3: 10 <= D1
s3 = subset(data, 10 < D1_radius)
# AREA
plot(s3$D1_radius, s3$RADIUS_AREA_CM, main="Section 3 (10 < D1): 
     D1 vs NODE_RADIUS_AREA", xlab="D1 (radius, cm)", 
     ylab="NODE_RADIUS_AREA (cm)")
line7 = lm(RADIUS_AREA_CM~D1_radius, data=s3)
abline(line7, col="red", lwd=2)
#residuals
residuals7 = residuals(line7)
mse7 = mean(residuals7^2) # mse = 1.488843
mae7 = mean(abs(residuals7)) # mae = 0.9293911
#summary
summary(line7)
#confidence interval
confint(line7)
#r^2
summary(line7)$r.squared # r^2 = 0.06134454
summary(line7)$adj.r.squared # 0.01664666

# CIRCUMFERENCE
plot(s3$D1_radius, s3$RADIUS_CIRC_CM, main="Section 3 (10 < D1): 
     D1 vs NODE_RADIUS_CIRCUMFERENCE", xlab="D1 (radius, cm)", 
     ylab="NODE_RADIUS_CIRCUMFERENCE (cm)")
line8 = lm(RADIUS_CIRC_CM~D1_radius, data=s3)
abline(line8, col="red",lwd=2)
#residuals
residuals8 = residuals(line8)
mse8 = mean(residuals8^2) # mse = 0.02591331
mae8 = mean(abs(residuals8)) # mae = 0.1181762
#summary
summary(line8)
#confidence interval
confint(line8)
#r^2
summary(line8)$r.squared # r^2 = 0.05664148
summary(line8)$adj.r.squared # 0.01171965



