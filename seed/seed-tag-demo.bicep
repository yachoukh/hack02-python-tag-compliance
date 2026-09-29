targetScope = 'resourceGroup'

param location string = 'swedencentral'

var purposeTag = {
  purpose: 'copilot-hackathon'
}

resource nsgCompliant 'Microsoft.Network/networkSecurityGroups@2024-05-01' = {
  name: 'nsg-tags-compliant-01'
  location: location
  tags: union(purposeTag, {
    owner: 'network@azultech.local'
    costCenter: 'CC-2001'
    environment: 'dev'
    application: 'tag-demo'
    dataClassification: 'internal'
  })
  properties: {
    securityRules: []
  }
}

resource routeCompliant 'Microsoft.Network/routeTables@2024-05-01' = {
  name: 'rt-tags-compliant-01'
  location: location
  tags: union(purposeTag, {
    owner: 'platform'
    costCenter: 'CC-2002'
    environment: 'test'
    application: 'routing-demo'
    dataClassification: 'public'
  })
  properties: {
    routes: []
  }
}

resource identityMissingTags 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: 'id-tags-missing-owner-cost'
  location: location
  tags: union(purposeTag, {
    environment: 'dev'
    application: 'identity-demo'
    dataClassification: 'internal'
  })
}

resource vnetInvalidEnvironment 'Microsoft.Network/virtualNetworks@2024-05-01' = {
  name: 'vnet-tags-invalid-env'
  location: location
  tags: union(purposeTag, {
    owner: 'network'
    costCenter: 'CC-2003'
    environment: 'Production'
    application: 'network-demo'
    dataClassification: 'confidential'
  })
  properties: {
    addressSpace: {
      addressPrefixes: [
        '10.42.0.0/24'
      ]
    }
    subnets: []
  }
}

resource storageInvalidCostCenter 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: toLower('st${uniqueString(resourceGroup().id)}tags')
  location: location
  tags: union(purposeTag, {
    owner: 'storage'
    costCenter: '1234'
    environment: 'prod'
    application: 'storage-demo'
    dataClassification: 'confidential'
  })
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
  }
}

resource nsgPurposeOnly 'Microsoft.Network/networkSecurityGroups@2024-05-01' = {
  name: 'nsg-tags-purpose-only'
  location: location
  tags: purposeTag
  properties: {
    securityRules: []
  }
}
