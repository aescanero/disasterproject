# disasterproject
Code examples for disaterproject blog (www.disaserproject.com)

## Entorno Ansible para el despliegue de entornos de pruebas/demo con KVM

El fichero inventory.yml define las máquinas que van a ser lanzadas y tiene la siguiente definición:

```yaml
all:
  children:
    vms:
      hosts:
        MACHINE_NAME1:
          memory: MEMORY_IN_MB
          vcpus: vCPUS_FOR_VM
          vm_ip: "IP_VM_MACHINA_NAME1"
          linux_flavor: "debian|centos"
          container_engine: "docker|podman"
        MACHINE_NAME2:
          memory: MEMORY_IN_MB
          vcpus: vCPUS_FOR_VM
          vm_ip: "IP_VM_MACHINA_NAME2"
          linux_flavor: "debian|centos"
          container_engine: "docker|podman"
      vars:
        network_name: NETWORK_NAME
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


