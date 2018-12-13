from mininet.topo import Topo

class MyTopo( Topo ):
    def __init__( self ):
        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        leftHost1 = self.addHost( 'h1' )
        LeftHost2 = self.addHost( 'h2' )
        rightHost1 = self.addHost( 'h3' )
        rightHost2 = self.addHost( 'h4' )
        leftSwitch = self.addSwitch( 's1' )
        rightSwitch = self.addSwitch( 's2' )

        # Add links
        self.addLink( leftHost1, leftSwitch )
        self.addLink( LeftHost2, leftSwitch )
        self.addLink( leftSwitch, rightSwitch )
        self.addLink( rightHost1, rightSwitch )
        self.addLink( rightHost2, rightSwitch )


topos = { 'mytopo': ( lambda: MyTopo() ) }
