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
a=`echo "$((${-+"(${IP_POOL_LOW//./"+256*("}))))"}&255))"`
b=`echo "$((${-+"(${IP_POOL_LOW//./"+256*("}))))"}>>8&255))"`
c=`echo "$((${-+"(${IP_POOL_LOW//./"+256*("}))))"}>>16&255))"`

for i in $(seq $low $high)
do
  ip="${a}.${b}.${c}.${i}"
  echo $ip
  json='{"address": "'"${ip}"'"}'
  echo $json
  curl -d "$json" -H 'Content-Type: application/json' http://api:8080/v2/ips
done
