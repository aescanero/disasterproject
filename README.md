# disasterproject
Code examples for disaterproject blog (www.disaserproject.com)

## Entorno Ansible para el despliegue de entornos de máquinas virtuales para pruebas/demo con KVM

El fichero inventory.yml define las máquinas virtuales que van a ser lanzadas y tiene la siguiente definición:

```yaml
all:
  children:
    vms:
      hosts:
        MACHINE_NAME1:
          memory: MEMORY_IN_MB
          vcpus: vCPUS_FOR_VM
          vm_ip: "IP_VM_MACHINE_NAME1"
          linux_flavor: "debian|centos"
        MACHINE_NAME2:
          memory: MEMORY_IN_MB
          vcpus: vCPUS_FOR_VM
          vm_ip: "IP_VM_MACHINE_NAME2"
          linux_flavor: "debian|centos"
      vars:
        domain: FQDN_DOMAIN
        network: "VM_NETWORK"
```

Existen algunas variables globales que cuelgan de "vars:", que son:

* network_name: Nombre descriptivo de la red de libvirt que crearemos y que además será el nombre del interface que se configurará en el anfitrión KVM y que servirá de puerta de enlace de las máquinas virtuales
* network: los tres primeros campos de la dirección IPv4 para confirmar una red con máscara 255.255.255.0, las máquinas virtuales deberán tener una IP de dicho rango (menos 0,1 y 255)

El formato de cada equipo cuelga se define por los siguientes atributos:

* nombre: Nombre descriptivo de la máquina virtual a desplegar, será además el hostname del equipo
* memory: Memoria de la máquina virtual en MB
* vcpus: Número de CPUs virtuales en la máquina virtual
* vm_ip: IP de la máquina virtual, debe pertenecer al rango definido en la variable general "network"
* linux_flavor: Es la distribución de la máquina virtual, se permiten dos opciones: debian y centos
* container_engine: (Opcional) Es el motor de contenedores que se puede desplegar en la máquina virtual, se permiten dos opciones: docker y podman 

Se ejecuta con 
```
$ ansible-playbook -i inventory.yml create.yml -K
```
Se elimina con 
```
$ ansible-playbook -i inventory.yml destroy.yml -K
```
Se guarda con 
```
$ ansible-playbook -i inventory.yml hibernate.yml -K
```
Se restaura con 
```
$ ansible-playbook -i inventory.yml restore.yml -K
```

Se accede a la MV con:
```
$ chmod 600 files/insecure_private_key
$ ssh -i files/insecure_private_key -o StrictHostKeyChecking=no vagrant@IP_VM
```

## Kubernetes

### Entorno Ansible para el despliegue de entornos de máquinas virtuales con Kubernetes, containerd, metallb (balanceador) y weave (gestión de red) para pruebas/demo con KVM y pods 

El fichero inventory.kubernetes.yml define las máquinas virtuales que van a ser lanzadas, modificando el atributo container_engine para elegir el motor de contenedores y tiene la siguiente definición:

```yaml
all:
  children:
    vms:
      hosts:
        MACHINE_NAME1:
          memory: MEMORY_IN_MB
          vcpus: vCPUS_FOR_VM
          vm_ip: "IP_VM_MACHINE_NAME1"
          linux_flavor: "debian|centos"
          container_engine: "kubernetes"
        MACHINE_NAME2:
          memory: MEMORY_IN_MB
          vcpus: vCPUS_FOR_VM
          vm_ip: "IP_VM_MACHINE_NAME2"
          linux_flavor: "debian|centos"
          container_engine: "kubernetes"
      vars:
        domain: FQDN_DOMAIN
        network: "VM_NETWORK"
        ingress:
        - traefik
        addons:
        - name: externaldns
          publish:
          - route
          - external
        - name: k8dash
          publish:
          - route
        - name: weave-scope
          publish:
          - route
        - name: dashboard
          publish:
          - route
        - name: kube-ops-view
          publish:
          - route
        - name: kubeview
          publish:
          - route
```

Se ejecuta con 
```
$ ansible-playbook -i inventory.kubernetes.yml create.yml -K
```
Se elimina con 
```
$ ansible-playbook -i inventory.kubernetes.yml destroy.yml -K
```
Se guarda con 
```
$ ansible-playbook -i inventory.kubernetes.yml hibernate.yml -K
```
Se restaura con 
```
$ ansible-playbook -i inventory.kubernetes.yml restore.yml -K
```

Se accede a la MV con:
```
$ chmod 600 files/insecure_private_key
$ ssh -i files/insecure_private_key -o StrictHostKeyChecking=no vagrant@IP_VM
```

## K3s

### Entorno Ansible para el despliegue de entornos de máquinas virtuales con K3s, metallb (balanceador) y flannel (gestión de red), sin servicelb, para pruebas/demo con KVM y pods

El fichero inventory.k3s.yml define las máquinas virtuales que van a ser lanzadas, modificando el atributo container_engine para elegir el motor de contenedores y tiene la siguiente definición:

```yaml
all:
  children:
    vms:
      hosts:
        MACHINE_NAME1:
          memory: MEMORY_IN_MB
          vcpus: vCPUS_FOR_VM
          vm_ip: "IP_VM_MACHINE_NAME1"
          linux_flavor: "debian|centos"
          container_engine: "k3s"
        MACHINE_NAME2:
          memory: MEMORY_IN_MB
          vcpus: vCPUS_FOR_VM
          vm_ip: "IP_VM_MACHINE_NAME2"
          linux_flavor: "debian|centos"
          container_engine: "k3s"
      vars:
        domain: FQDN_DOMAIN
        network: "VM_NETWORK"
        ingress:
        - traefik
        addons:
        - name: externaldns
          publish:
          - route
          - external
        - name: k8dash
          publish:
          - route
        - name: weave-scope
          publish:
          - route
        - name: dashboard
          publish:
          - route
        - name: kube-ops-view
          publish:
          - route
        - name: kubeview
          publish:
          - route
```

Se añade la variable global opcional: addons para añadir ciertas caracteristicas a la demo como pueden ser acceso al interfaz web de
Traefik, los dashboards scope o k8dash, configurar external-dns para poder resolver las rutas de traefik o instalar el microPaaS RIO

* ingress: OPCIONAL, Por defecto traefik
  * "traefik" para instalar traefix como ingress (endpoind de la plataforma) y acceder a la interfaz web de traefik (http://IP_service_traefik:8080, username admin, password admin)

* addons: OPCIONAL, es una lista que puede contener al menos alguno de los siguientes valores:
  * "k8dash" para activar el dashboard y disponer de visibilidad sobre la plataforma
  * "weave-scope" un potente dashboard que relaciona los elementos de la plataforma
  * "rio" para instalar el microPaaS RIO junto con k3s
  * "externaldns", configura un servicio para resolución DNS de traefik, incluye PowerDNS y PowerDNS-Admin para acceder a PowerDNS y ver que registros existen.

Se ejecuta con 
```
$ ansible-playbook -i inventory.k3s.yml create.yml -K
```
Se elimina con 
```
$ ansible-playbook -i inventory.k3s.yml destroy.yml -K
```
Se guarda con 
```
$ ansible-playbook -i inventory.k3s.yml hibernate.yml -K
```
Se restaura con 
```
$ ansible-playbook -i inventory.k3s.yml restore.yml -K
```

Se accede a las Máquinas virtuales con:
```
$ chmod 600 files/insecure_private_key
$ ssh -i files/insecure_private_key -o StrictHostKeyChecking=no vagrant@IP_VM
```

