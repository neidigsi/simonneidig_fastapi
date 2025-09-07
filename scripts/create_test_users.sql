INSERT INTO postgres."user"
(id, email, hashed_password, is_active, is_superuser, is_verified)
VALUES('3e98d38d-abd5-48a7-b3a8-449a46f0dc1c'::uuid, 'test@simon-neidig.eu', '$argon2id$v=19$m=65536,t=3,p=4$sxYXzoo116TYwN9pKlOfXw$x+J4qAbl3oQ5A2KMLQUwhX/jaJts4QgSWcBp8VLZ6N0', true, true, true);
INSERT INTO postgres."user"
(id, email, hashed_password, is_active, is_superuser, is_verified)
VALUES('9d9d2265-07ac-48d5-af14-a56e93233f04'::uuid, 'nonadmin@simon-neidig.eu', '$argon2id$v=19$m=65536,t=3,p=4$ZFtNuFL5zDG629ZUhqlkaA$9gWoPJswDHqH7gJhCmf6v6U31SNlIku46xFuvjYCe5A', true, false, false);