
static constexpr std::uint32_t hash = Transformer::get_hash_value() ^ Arch::get_hash_value();


static constexpr std::uint32_t Transformer::get_hash_value() {
  return (UseThreats ? ThreatFeatureSet::HashValue : PSQFeatureSet::HashValue)
  ^ (OutputDimensions * 2);


  1082167927 ^ (3072 * 2)


  PSQFeatureSet::HashValue == 1082167927;
                              1082167927

  OutputDimensions == 3072; 3072;
}


getting 2401457336 // because we're using treats

should get  1082165879
            1082165879
