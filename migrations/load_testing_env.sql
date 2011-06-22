-- Script to load testing data into the Gateway
-- load default user so i can login

DELETE FROM groups;
INSERT INTO groups VALUES
(1, 'admin');

DELETE FROM users;
INSERT INTO users VALUES
(1 , 'admin', '48dc53f1fe20e666d2dadb1aeb0ce431', 'iwillig@gmail.com', 't', 1);

-- load commuication interface
DELETE FROM communication_interface;
INSERT INTO communication_interface  VALUES 
(
   'netbook_interface',  
    1, 
    'Testing Interface', 
    'Modi Labs', 
    'New York City' , 
    '13473529231'
);

-- add the twilio type
DELETE FROM netbook_interface;
INSERT INTO netbook_interface VALUES
(1); 


DELETE FROM meter;
INSERT INTO meter VALUES 
(1 , 
   '6b7a5d09-b73e-4ae1-b4ba-cf5d6dab85a0', 
   'demo001',
   '+13474594049',
   'New York City' , 
   't', 
   '2010-12-18 19:31:17', 
   100, 
   100, 
   'POINT (1 1)', 1);

DELETE FROM devices; 
INSERT INTO devices VALUES
(1, 'abc123', '48dc53f1fe20e666d2dadb1aeb0ce431');

DELETE FROM account;
INSERT INTO account VALUES (28, 'default', '', 'en');
INSERT INTO account VALUES (26, 'default', '+13479440686', 'en');
INSERT INTO account VALUES (27, 'default', '+13479440686', 'en');
INSERT INTO account VALUES (29, 'default', '+13479440686', 'en');
INSERT INTO account VALUES (31, 'default', '+13479440686', 'en');
INSERT INTO account VALUES (32, 'default', '+13479440686', 'en');
INSERT INTO account VALUES (33, 'default', '+13479440686', 'en');
INSERT INTO account VALUES (34, 'default', '+13479440686', 'en');
INSERT INTO account VALUES (35, 'default', '+13479440686', 'en');
INSERT INTO account VALUES (36, 'default', '+13479440686', 'en');
INSERT INTO account VALUES (37, 'default', '13479440686', 'en');
INSERT INTO account VALUES (38, 'default', '+13479440686', 'en');
INSERT INTO account VALUES (39, 'default', '+13479440686', 'en');
INSERT INTO account VALUES (40, 'default', '+13479440686', 'en');
INSERT INTO account VALUES (41, 'default', '+13479440686', 'en');
INSERT INTO account VALUES (42, 'default', '+13479440686', 'en');
INSERT INTO account VALUES (43, 'default', '+13479440686', 'en');
INSERT INTO account VALUES (44, 'default', '+13479440686', 'en');
INSERT INTO account VALUES (45, 'default', '+13479440686', 'en');
INSERT INTO account VALUES (46, 'default', '+13479440686', 'en');
INSERT INTO account VALUES (47, 'default', '+13479440686', 'en');
INSERT INTO account VALUES (48, 'default', '', 'en');
INSERT INTO account VALUES (30, 'default', '+19177275752', 'en');
INSERT INTO account VALUES (49, 'default', '', 'en');
INSERT INTO account VALUES (51, 'default', '', 'en');



DELETE FROM circuit;

INSERT INTO circuit VALUES (48, '4c0beec8-5fa8-4e1b-a5c2-1bb55cb6e41f', '2011-03-30 17:43:53.880508', 'a', 1, 100, 100, 1, '192.168.1.200', 0, 48);
INSERT INTO circuit VALUES (26, '4bf99cb3-6fa7-401f-88e0-46091f7f3412', '2010-12-18 19:31:24.000485', 'b', 1, 100, 100, 1, '192.168.1.201', 0, 26);
INSERT INTO circuit VALUES (27, '1b0817ab-1bf7-47a7-b944-2cc378dc7bab', '2010-12-21 16:06:38.543737', 'c', 1, 100, 100, 0, '192.168.1.202', 0, 27);
INSERT INTO circuit VALUES (29, '9c45b7cc-a8d4-477b-a622-d9ef8186203b', '2010-12-21 16:06:53.446598', 'd', 1, 100, 100, 0, '192.168.1.203', 0, 29);
INSERT INTO circuit VALUES (30, 'e3256841-1b13-4222-b3c9-075854e67b8a', '2010-12-21 16:18:53.81113',  'e', 1, 100, 100, 0, '192.168.1.204', 0, 30);
INSERT INTO circuit VALUES (31, '232535b4-cf02-4e13-83bd-c5358fd8b209', '2010-12-21 16:19:11.805201', 'f', 1, 100, 100, 0, '192.168.1.205', 0, 31);
INSERT INTO circuit VALUES (32, '6efeefcf-9030-4fd2-88f2-9f2d8d51f6bf', '2010-12-21 16:20:14.940787', 'g', 1, 100, 100, 0, '192.168.1.206', 0, 32);
INSERT INTO circuit VALUES (33, '019a7314-1389-4f60-97e8-1cfadcc3a92c', '2010-12-21 16:20:26.969001', 'h', 1, 100, 100, 0, '192.168.1.207', 0, 33);
INSERT INTO circuit VALUES (45, '8fa299b6-ae57-4296-9fcd-596320de4959', '2011-01-28 20:06:03.426939', 'i', 1, 100, 100, 1, '192.168.1.208', 0, 45);
INSERT INTO circuit VALUES (46, 'b532869e-0ab3-4137-b75a-37fc23b616f2', '2011-01-28 20:06:16.827843', 'j', 1, 100, 100, 1, '192.168.1.209', 0, 46);
INSERT INTO circuit VALUES (36, '135fc0b0-c427-4358-9080-4a7783184ef8', '2010-12-21 16:21:37.602078', 'k', 1, 100, 100, 0, '192.168.1.210', 0, 36);
