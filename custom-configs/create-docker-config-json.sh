kubectl create secret docker-registry docker-pass \
--docker-server='https://index.docker.io/v1/' \
--docker-username='user' --docker-password='pass' \
--docker-email='email' \
-n kafka