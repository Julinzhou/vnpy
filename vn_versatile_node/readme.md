vn_versatile_node

多用途节点

一个节点只有一个角色，要么是策略(附带回测功能)，要么是交易接口，听取策略的订单，启动时加载配置文件，决定此节点扮演什么角色。
既然叫做节点，自然就要设计成能够资辞多核多机以及docker容器运行的功能
