# Основное


## Поиск совпадений по тексту всех файлов текущей директории
`grep -rni {patter_string: "string"} *`

## Визуализация состояний git и k8s в информационной строке терминала
* Добавить скрипт визуализации в `~/.bashrc`;
* Скрипт вызуализации:
```Bash
{                                                                                                                                                                                           
	  CONTEXT=$(cat ~/.kube/config | grep "current-context:" | sed "s/current-context: //")
	  if [ "$CONTEXT" -eq "yc-asgard" ]; then
	    echo "(KUBER-PROD!)"                                                                                                             
	  fi
	  if [ "$CONTEXT" == "yc-midgard" ]; then
	    echo "(KUBER-stage)"                                                                                                             
	  fi  
	  if [ "$CONTEXT" == "minikube" ]; then
	    echo "(KUBER-minikube)"                                                                                                             
	  fi  
	}  
	parse_git_branch() {
 git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/'
}  
```