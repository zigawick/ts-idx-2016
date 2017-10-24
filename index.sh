if [[ "$1" == "varbyte" ]]; then
  python2.7 index_var.py "${@:2}"
  echo "python2.7 index_read_var.py “\$@“" > search.sh
else
  python2.7 index_simple.py "${@:2}"
  echo "python2.7 index_read_simple.py “\$@“" > search.sh
fi

chmod +x search.sh
