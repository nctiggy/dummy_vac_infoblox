function get_last {
  a=$1; div='.'; set --
  while
    b=${a#*"$div"}
    set -- "$@" "${a%%"$div"*}"
    [ "$a" != "$b" ]
    do
      a=$b
    done
  eval last=\${$#}
  echo $last
}

low=`get_last $IP_POOL_LOW`
high=`get_last $IP_POOL_HIGH`

sleep 10

for i in $(seq $low $high)
do
  ip="192.168.0.${i}"
  echo $ip
  json='{"address": "'"${ip}"'"}'
  echo $json
  curl -d "$json" -H 'Content-Type: application/json' http://api:8080/v2/ips
done
